import universaldatatool as udt
from universaldatatool.nb.LocalFileProxyServer import LocalFileProxyServer
from universaldatatool.nb.Session import local_file_proxy_server
from os import path
import requests


class TestLocalFileProxyServer(object):
    def test_localfileproxy_server(self):
        server = LocalFileProxyServer()
        testfile_content = open(
            path.join(path.dirname(__file__), "testfile.txt"), "rb"
        ).read()
        server.start(
            "test_client_id", {"test_file_id.txt": testfile_content},
        )
        file_content = requests.get(
            "https://localfileproxy.universaldatatool.com/test_client_id/test_file_id.txt"
        )
        assert file_content.text == testfile_content.decode("ascii")

        server.stop()
