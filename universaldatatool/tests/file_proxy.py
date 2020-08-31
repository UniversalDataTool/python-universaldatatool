from universaldatatool.nb.PublicFileProxy import PublicFileProxy
from os import path
import requests
import time


testfile_path = "file://" + path.join(path.dirname(__file__), "testfile.txt")
testimage_path = "file://" + path.join(
    path.dirname(__file__), "../../cypress/assets/bird.jpg"
)


class TestEmitterLocalFileProxyServer(object):
    def test_localfileproxy_server(self):
        server = PublicFileProxy()
        server.start()

        # file_url = server.get_proxied_file_url(testfile_path)
        # print(file_url)
        # print(testfile_path)
        # file_content = requests.get(file_url)
        # print(file_content.text)
        # assert file_content.text == open(testfile_path[7:], "rb").read().decode("ascii")
        # print("text file complete")

        file_url = server.get_proxied_file_url(testimage_path)
        print(file_url)
        print(testimage_path)
        file_content = requests.get(file_url)
        print("got image")
        print(len(file_content.content))
        if len(file_content.content) < 1000:
            print(file_content.content)

        server.stop()
