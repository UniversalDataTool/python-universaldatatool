from universaldatatool.nb.ZMQLocalFileProxyServer import ZMQLocalFileProxyServer
from os import path
import requests
import time


testfile_path = "file://" + path.join(path.dirname(__file__), "testfile.txt")


class TestZMQLocalFileProxyServer(object):
    def test_localfileproxy_server(self):
        server = ZMQLocalFileProxyServer()
        server.start()

        file_url = server.get_proxied_file_url(testfile_path)
        print(testfile_path)
        print(file_url)
        time.sleep(1)

        file_content = requests.get(file_url)
        print(file_content.text)
        assert file_content.text == open(testfile_path[7:], "rb").read().decode("ascii")

        server.stop()
