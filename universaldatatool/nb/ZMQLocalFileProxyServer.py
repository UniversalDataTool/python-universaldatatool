import zmq
from os import path
import threading
import time


class ZMQLocalFileProxyServer(object):
    def __init__(self):
        self.running = False

    def send_heartbeat(self):
        self.socket.send_multipart(
            [b"", b"client_service_heartbeat", self.client_id.encode("ascii")]
        )

    def send_heartbeat_every_5s(self):
        while self.running:
            self.send_heartbeat()
            for i in range(100):
                if not self.running:
                    break
                time.sleep(5 / 100)

    def send_file(self, file_id):
        if file_id in self.file_id_path_map:
            self.socket.send_multipart(
                [
                    b"",
                    b"file",
                    self.client_id.encode("ascii"),
                    file_id.encode("ascii"),
                    open(self.file_id_path_map[file_id], "rb").read(),
                ]
            )

    def start(self, client_id, file_id_path_map):
        self.client_id = client_id
        self.file_id_path_map = file_id_path_map
        self.running = True
        context = zmq.Context()
        self.socket = context.socket(zmq.DEALER)

        self.socket.connect("tcp://localfileproxy.universaldatatool.com:2900")

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
