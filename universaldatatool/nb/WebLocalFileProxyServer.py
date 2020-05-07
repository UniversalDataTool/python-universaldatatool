import time
import web
import threading


class WebLocalFileProxyServer(object):
    def __init__(self):
        self.app = None
        self.running = False

    def start(self, file_id_path_map):
        if self.app is not None:
            self.stop()

        self.file_id_path_map = file_id_path_map
        self.running = True

        self.serve_files_thread = threading.Thread(
            name="serve_files", target=self.serve_files
        )

        self.serve_files_thread.start()

    def serve_files(server):
        class serve_file:
            def GET(req):
                file_path = server.file_id_path_map.get(web.ctx.path[1:], None)
                if file_path is None:
                    raise web.HTTPError("404 not found")
                return open(file_path, "rb").read()

        server.app = web.application(("/.*", "serve_file"), {"serve_file": serve_file})
        server.app.run()

    def stop(self):
        print("attempting to stop...")
        self.running = False
        self.app.stop()
        print("joining thread...")
        self.serve_files_thread.join()
        self.app = None

    # def serve_files(server):
    #     class web_app(web.application):
    #         def __init__(self):
    #             super().__init__(("/.*", "serve_file"), {"serve_file": self.serve_file})
    #
    #         def run(self, port=9090):
    #             func = self.wsgifunc()
    #             return web.httpserver.runsimple(func, ("0.0.0.0", port))
    #
    #         def serve_file(web_app):
    #             def GET(req):
    #                 file_path = server.file_id_path_map.get(web.ctx.path[1:], None)
    #                 if file_path is None:
    #                     raise web.HTTPError("404 not found")
    #                 return open(file_path, "rb").read()
    #
    #     server.app = web_app()
    #     server.app.run()


if __name__ == "__main__":
    server = WebLocalFileProxyServer()
    server.start({"bird.jpg": "/home/seve/downloads/birds/good_bird.jpg"})
    time.sleep(5)
    server.stop()
