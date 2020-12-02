from typing import Optional, Awaitable

import tornado.ioloop
import tornado.web
import tornado.options
import tornado.httpserver

from tornado.options import define, options

import os.path


class MainHandler(tornado.web.RequestHandler):
    def data_received(self, chunk: bytes) -> Optional[Awaitable[None]]:
        pass

    def get(self):
        self.write("Hello, world")


define("port", default=8000, help="run on the given port", type=int)

if __name__ == "__main__":

    tornado.options.parse_command_line()

    settings = {
        "template_path": os.path.join(os.path.dirname(__file__), "templates"),
        "static_path": os.path.join(os.path.dirname(__file__), "static"),
        # "cookie_secret": "s8iJWyTeSQ+Hfgj59nTy4bFKahPdAEnbhsH5CRuUN1g=",
        # "login_url": "/login",
        # "db": db,
        "debug": True,
        # "xsrf_cookies": True

    }

    app = tornado.web.Application([
        (r"/", MainHandler),
        ],
        **settings
        )

    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)

    try:
        tornado.ioloop.IOLoop.current().start()

    except KeyboardInterrupt:
        print('Server has shut down.')
