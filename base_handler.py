import tornado.web
from typing import Optional, Awaitable

import jwt

SECRET_KEY = 'zmd4yAQoTM2VpKwpnJkac2ud5I0U30mDqSLsPq4ZBbI='
API_KEY = '4925348b1e47840c593327c7a0578ce79d50f4ee'


class BaseHandler(tornado.web.RequestHandler):

    # suggested by pycharm for warning repression
    def data_received(self, chunk: bytes) -> Optional[Awaitable[None]]:
        pass

    def prepare(self):
        if self.get_argument("btn1", None) is not None:
            print("detected click on btn Profile")
            self.redirect("/profile")
            return

        if self.get_argument("btn2", None) is not None:
            print("detected click on btn Profile")
            self.redirect("/")
            return

        if self.get_argument("logout", None) is not None:
            self.clear_cookie("token")
            self.redirect("/")
            return

        if self.get_argument("btnSignIn", None) is not None:
            print("detected click on btnSignIn")
            self.redirect("/signin")
            return

    def get_current_user(self):
        token = self.get_secure_cookie('token', None)
        print("token: ", token)

        if token:
            try:
                data = jwt.decode(token, SECRET_KEY)
            except jwt.DecodeError as e:
                print("An error occurred while decoding: ", e)
                return None
            else:
                return data

        return token
