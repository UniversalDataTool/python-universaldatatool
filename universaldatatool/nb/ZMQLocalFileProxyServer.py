import zmq
from os import path
import threading
import time
import string
import random
import posixpath
import re
from base64 import b64encode

public_local_file_proxy_server = "https://localfileproxy.universaldatatool.com"
# public_local_file_proxy_server = "http://localhost:3000"
secret = b"default_secret"


def random_string(stringLength=8):
    letters = string.ascii_lowercase + string.digits + string.ascii_uppercase
    return "".join(random.choice(letters) for i in range(stringLength))


class ZMQLocalFileProxyServer(object):
    def __init__(self):
        self.running = False
        self.file_id_to_path = {}
        self.file_url_to_proxied_url = {}
        self.proxied_url_to_file_url = {}
        self.client_id = random_string(16)

    def send_heartbeat(self):
        self.socket.send_multipart(
            [b"", b"client_service_heartbeat", self.client_id.encode("ascii"), secret]
        )

    def send_heartbeat_every_5s(self):
        while self.running:
            self.send_heartbeat()
            for i in range(100):
                if not self.running:
                    break
                time.sleep(5 / 100)

    def send_file(self, file_id):
        print("sending file " + file_id)
        if file_id in self.file_id_to_path:
            self.socket.send_multipart(
                [
                    b"",
                    b"file",
                    self.client_id.encode("ascii"),
                    file_id.encode("ascii"),
                    open(self.file_id_to_path[file_id], "rb").read(),
                ]
            )

    def get_addr(self, file_id):
        return "{}/{}/{}".format(
            public_local_file_proxy_server, self.client_id, file_id
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
        return proxied_url

    def start(self):
        self.running = True
        context = zmq.Context()
        self.socket = context.socket(zmq.DEALER)

        self.socket.connect(
            "tcp://{}:2900".format(
                re.search("https?://([^:]*)", public_local_file_proxy_server).group(1)
            )
        )

        self.send_heartbeat()

        self.heartbeat_thread = threading.Thread(
            name="poll_heartbeat", target=self.send_heartbeat_every_5s
        )
        self.serve_files_thread = threading.Thread(
            name="serve_files", target=self.serve_files
        )

        self.heartbeat_thread.start()
        self.serve_files_thread.start()

    def serve_files(self):
        packet = []
        while self.running:
            try:
                request = self.socket.recv(flags=zmq.NOBLOCK)
                packet.append(request)
                if self.socket.get(zmq.RCVMORE) == 0:
                    (header, client_id, file_id) = packet[1:]
                    if client_id == self.client_id.encode("ascii"):
                        self.send_file(file_id.decode("ascii"))
                    packet = []
            except zmq.Again as e:
                time.sleep(0.01)

    def stop(self):
        self.running = False
        self.socket.close()
        self.serve_files_thread.join()
        self.heartbeat_thread.join()
