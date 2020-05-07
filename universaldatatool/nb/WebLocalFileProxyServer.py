import time
import web
import threading

running_web_file_proxies = []


class WebLocalFileProxyServer(object):
    def __init__(self):
        self.app = None
        self.running = False
        self.port = None

    def start(self, file_id_path_map):
        global running_web_file_proxies
        if self.app is not None:
            self.stop()

        self.file_id_path_map = file_id_path_map
        self.running = True

        self.serve_files_thread = threading.Thread(
            name="serve_files", target=self.serve_files
        )

        self.serve_files_thread.start()

    def serve_files(server):
        global running_web_file_proxies

        class serve_file:
            def GET(req):
                file_path = server.file_id_path_map.get(web.ctx.path[1:], None)
                if file_path is None:
                    raise web.HTTPError("404 not found")
                return open(file_path, "rb").read()

        server.app = web.application(("/.*", "serve_file"), {"serve_file": serve_file})
        # TODO find random available port or kill any other running server
        next_available_port = 9020
        if len(running_web_file_proxies) > 0:
            highest_port = max([p.port for p in running_web_file_proxies])
            if highest_port is not None:
                next_available_port = highest_port + 1
        server.port = next_available_port
        web.httpserver.runsimple(
            server.app.wsgifunc(), ("0.0.0.0", next_available_port)
        )

    def stop(self):
        print("attempting to stop...")
        self.running = False
        self.app.stop()
        print("joining thread...")
        self.serve_files_thread.join()
        self.app = None


if __name__ == "__main__":
    server = WebLocalFileProxyServer()
    server.start({"bird.jpg": "/home/seve/downloads/birds/good_bird.jpg"})
    time.sleep(5)
    server.stop()
