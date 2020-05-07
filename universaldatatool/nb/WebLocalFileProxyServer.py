import time
import web
import threading

running_web_file_proxies = []


class WebLocalFileProxyServer(object):
    def __init__(self):
        self.app = None
        self.running = False
        self.port = None
        self.file_id_to_path = {}
        self.file_url_to_proxied_url = {}
        self.proxied_url_to_file_url = {}

    def start(self):
        global running_web_file_proxies
        if self.app is not None:
            self.stop()

        if len(running_web_file_proxies) > 5:
            running_web_file_proxies[0].stop()
            running_web_file_proxies.pop(0)

        self.running = True

        self.serve_files_thread = threading.Thread(
            name="serve_files", target=self.serve_files
        )

        self.serve_files_thread.start()

    def get_next_available_port(self):
        next_available_port = 9020
        if len(running_web_file_proxies) > 0:
            highest_port = max([p.port for p in running_web_file_proxies])
            if highest_port is not None:
                next_available_port = highest_port + 1
        return next_available_port

    def get_addr(self, file_id):
        if self.port is None:
            return "http://localhost:{}/{}".format(
                self.get_next_available_port(), file_id
            )
        else:
            return "http://localhost:{}/{}".format(self.port, file_id)

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

    def serve_files(server):
        global running_web_file_proxies

        class serve_file:
            def GET(req):
                file_path = server.file_id_to_path.get(web.ctx.path[1:], None)
                if file_path is None:
                    raise web.HTTPError("404 not found")
                return open(file_path, "rb").read()

        server.app = web.application(("/.*", "serve_file"), {"serve_file": serve_file})
        # TODO find random available port or kill any other running server
        self.get_next_port()
        server.port = next_available_port
        web.httpserver.runsimple(
            server.app.wsgifunc(), ("0.0.0.0", next_available_port)
        )

    def stop(self):
        print("attempting to stop...")
        self.running = False
        running_web_file_proxies.pop(running_web_file_proxies.index(self))
        self.app.stop()
        print("joining thread...")
        self.serve_files_thread.join()
        self.app = None


if __name__ == "__main__":
    server = WebLocalFileProxyServer()
    server.start({"bird.jpg": "/home/seve/downloads/birds/good_bird.jpg"})
    time.sleep(5)
    server.stop()
