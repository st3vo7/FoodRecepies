import os.path

# import tornado.httpserver
# import tornado.ioloop
# import tornado.options

from recipe_handlers import *
from tornado.options import define, options

define("port", default=8000, help="run on the given port", type=int)


if __name__ == "__main__":

    tornado.options.parse_command_line()

    # create tables in db
    print("create_table()")
    create_table()

    settings = {
        "template_path": os.path.join(os.path.dirname(__file__), "templates"),
        "static_path": os.path.join(os.path.dirname(__file__), "static"),
        "cookie_secret": "s8iJWyTeSQ+Hfgj59nTy4bFKahPdAEnbhsH5CRuUN1g=",
        "login_url": "/login",
        # "db": db,
        "debug": True,
        # "xsrf_cookies": True

    }

    app = tornado.web.Application([
        (r"/", MainHandler),
        (r"/profile", ProfileHandler),
        (r"/create", CreateHandler),
        (r"/login", LoginHandler),
        ],
        **settings
        )

    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)

    try:
        tornado.ioloop.IOLoop.current().start()

    except KeyboardInterrupt:
        print('Server has shut down.')
