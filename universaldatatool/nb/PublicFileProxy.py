import requests
from os import path
import time
import string
import random
import posixpath
import time
import re
from base64 import b64encode
import threading
import warnings

public_proxy_url = "https://emitterfileproxy.universaldatatool.com"
# public_proxy_url = "http://localhost:3000"


def random_string(stringLength=8):
    letters = string.ascii_lowercase + string.digits + string.ascii_uppercase
    return "".join(random.choice(letters) for i in range(stringLength))


class PublicFileProxy(object):
    def __init__(self):
        self.running = False
        self.file_id_to_path = {}
        self.file_url_to_proxied_url = {}
        self.proxied_url_to_file_url = {}
        self.channel_id = None

    def get_addr(self, file_id):
        return "{}/api/{}/{}".format(public_proxy_url, self.channel_id, file_id)

    def get_proxied_file_url(self, file_url):
        if file_url in self.file_url_to_proxied_url:
            return self.file_url_to_proxied_url[file_url]

        extension = file_url.split(".")[-1]
        if len(extension) > 8 or "/" in extension:
            extension = ""
        file_name = file_url.split("/")[-1].split(".")[0]
        file_id = (
            random_string(8)
            + "_"
            + re.sub(r"[^a-zA-Z0-9_\-]", "", file_name)
            + "."
            + extension
        )
        proxied_url = self.get_addr(file_id)

        self.file_url_to_proxied_url[file_url] = proxied_url
        self.proxied_url_to_file_url[proxied_url] = file_url
        self.file_id_to_path[file_id] = file_url[len("file://") :]
        self.file_id_to_path[file_id.split(".")[0]] = file_url[len("file://") :]
        return proxied_url

    def poll_and_respond_to_requests(self):
        while self.running:
            res = requests.get(
                public_proxy_url + "/api/{}".format(self.channel_id)
            ).json()
            for fileid in res["requestedFiles"]:
                if not path.exists(self.file_id_to_path[fileid]):
                    warnings.warn("FILE DOES NOT EXIST (check the path): " + fileid)
                    continue
                requests.post(
                    public_proxy_url + "/api/{}/{}".format(self.channel_id, fileid),
                    files={"file": open(self.file_id_to_path[fileid], "rb")},
                )
            time.sleep(0.01)

    def start(self):
        self.running = True

        access = requests.get("{}/api/channel".format(public_proxy_url)).json()
        self.channel_id = access["channel"]
        self.channel_key = access["key"]

        self.thread = threading.Thread(
            target=self.poll_and_respond_to_requests, daemon=True
        )
        self.thread.start()

    def stop(self):
        self.running = False
