import requests
import json
import random
import string
import posixpath
from urllib.parse import urljoin
from base64 import b64encode
from .WebLocalFileProxyServer import WebLocalFileProxyServer
from .ZMQLocalFileProxyServer import ZMQLocalFileProxyServer


class ProxiedFileSession(object):
    def __init__(self, local_web_proxy=False):
        self.running = False
        self.local_web_proxy = local_web_proxy
        if local_web_proxy:
            self.file_proxy_server = WebLocalFileProxyServer()
        else:
            self.file_proxy_server = ZMQLocalFileProxyServer()
        self.get_proxied_file_url = self.file_proxy_server.get_proxied_file_url

    def start(self, dataset, local_web_proxy=False):
        self.running = True
        self.dataset = dataset
        dataset.file_session = self
        self.file_proxy_server.start()

    def stop(self):
        self.running = False
        if self.file_proxy_server is not None:
            self.file_proxy_server.stop()

    def set_client_id(self, client_id):
        # only valid for proxied file urls
        if not self.local_web_proxy:
            self.file_proxy_server.client_id = client_id
