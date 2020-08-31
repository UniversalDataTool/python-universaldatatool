from emitter import Client
import requests
from os import path
import time
import string
import random
import posixpath
import re
from base64 import b64encode

# public_local_file_proxy_server = "https://emitterfileproxy.universaldatatool.com"
public_local_file_proxy_server = "http://localhost:3000"


def random_string(stringLength=8):
    letters = string.ascii_lowercase + string.digits + string.ascii_uppercase
    return "".join(random.choice(letters) for i in range(stringLength))


class EmitterLocalFileProxyServer(object):
    def __init__(self):
        self.running = False
        self.file_id_to_path = {}
        self.file_url_to_proxied_url = {}
        self.proxied_url_to_file_url = {}
        self.channel_id = None

    def get_addr(self, file_id):
        return "{}/api/{}/{}".format(
            public_local_file_proxy_server, self.channel_id, file_id
        )

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

    def start(self):
        self.running = True

        access = requests.get(
            "{}/api/channel".format(public_local_file_proxy_server)
        ).json()
        self.channel_id = access["channel"]
        self.channel_key = access["key"]

        self.emitter = Client()

        # TODO emitter server should be configurable
        self.emitter.connect(
            host="emitter.universaldatatool.com", port=8080, secure=False,
        )
        self.emitter.subscribe(access["key"], access["channel"] + "/request")

        def respond_with_file(packet):
            file, respond_hash = packet.as_binary().decode("ascii").split(",")
            self.emitter.publish(
                access["key"],
                access["channel"] + "/" + respond_hash,
                open(self.file_id_to_path[file], "rb").read(),
            )

        self.emitter.on_message = respond_with_file
        self.emitter.loop_start()

        # TODO connect to emitter

    def stop(self):
        self.running = False
        self.emitter.loop_stop()
        self.emitter.disconnect()
