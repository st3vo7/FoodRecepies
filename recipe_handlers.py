from typing import Optional, Awaitable

import tornado.ioloop
import tornado.web
import tornado.options
import tornado.httpserver


class MainHandler(tornado.web.RequestHandler):
    def data_received(self, chunk: bytes) -> Optional[Awaitable[None]]:
        pass

    def get(self):
        self.render('homepage.html')
