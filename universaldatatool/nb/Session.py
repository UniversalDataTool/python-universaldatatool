import requests
import json
import random
import string
import posixpath
from urllib.parse import urljoin

# TODO this should be configurable
collaborative_session_server = "https://udt-collaboration-server.now.sh"
local_file_proxy_server = "http://localhost:3000"


def random_string(stringLength=8):
    letters = string.ascii_lowercase + string.digits + string.ascii_uppercase
    return "".join(random.choice(letters) for i in range(stringLength))


class Session(object):
    def __init__(self):
        self.running = False
        self.file_url_to_proxied_url = {}
        self.proxied_url_to_file_url = {}

    def start(self, dataset):
        self.running = True
        self.dataset = dataset
        dataset.online_session = self
        self.localfileproxy_client_id = random_string(16)
        self.create_collaborative_session(dataset)

    def create_collaborative_session(self, dataset, proxy_files=False):
        req_url = "{}/{}".format(collaborative_session_server, "api/session")
        # TODO remove legacy dataset conversion when collaboartive server supports it
        response = requests.post(
            req_url,
            json={
                "udt": json.loads(
                    dataset.to_legacy_json_string(proxy_files=proxy_files, session=self)
                )
            },
        ).json()
        self.collab_session_id = response["short_id"]
        self.version = response["version"]

    def start_local_file_server(self):
        pass

    def get_proxied_file_url(self, file_url):
        proxied_url = self.file_url_to_proxied_url.get(file_url, None)
        if proxied_url is None:
            extension = file_url.split(".")[-1]
            if len(extension) > 8 or "/" in extension:
                extension = ""
            file_id = random_string(16) + "." + extension
            proxied_url = urljoin(
                local_file_proxy_server,
                posixpath.join(self.localfileproxy_client_id, file_id,),
            )
            print(proxied_url)
            self.file_url_to_proxied_url[file_url] = proxied_url
            self.proxied_url_to_file_url[proxied_url] = file_url
        return proxied_url

    def stop(self):
        self.running = False
