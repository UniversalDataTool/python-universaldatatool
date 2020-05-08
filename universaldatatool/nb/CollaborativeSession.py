import requests
import json
import random
import string
import posixpath
from urllib.parse import urljoin

# TODO this should be configurable
collaborative_session_server = "https://udt-collaboration-server.now.sh"


class CollaborativeSession(object):
    def __init__(self):
        self.running = False

    def start(self, dataset):
        self.running = True
        self.dataset = dataset
        dataset.collaborative_session = self
        self.create_collaborative_session(dataset)

    def create_collaborative_session(self, dataset, proxy_files=True):
        if not dataset.proxied_file_session:
            print("Can't proxy local files to collaborative session")
            proxy_files = False

        req_url = "{}/{}".format(collaborative_session_server, "api/session")
        # TODO remove legacy dataset conversion when collaboartive server supports it
        response = requests.post(
            req_url, json={"udt": dataset.to_dict(proxy_files=proxy_files)},
        ).json()
        self.collab_session_id = response["short_id"]
        self.version = response["version"]

    def stop(self):
        self.running = False

    def sync_changes(self):
        if not self.running:
            raise "Not running"

        response = requests.get(
            "{}/{}/{}".format(
                collaborative_session_server, "/api/session", self.collab_session_id
            )
        ).json()

        latest_udt = response["udt_json"]
        if "samples" not in latest_udt or "interface" not in latest_udt:
            return

        for i, sample in enumerate(latest_udt["samples"]):
            if "annotation" in sample:
                self.dataset.samples[i].annotation = sample["annotation"]
