from base_handler import *


class MainHandler(BaseHandler):

    def get(self):
        self.render('homepage.html')


class ProfileHandler(BaseHandler):

    def prepare(self):
        super().prepare()

    # @tornado.web.authenticated
    def get(self):

        """
        my_db = self.settings['db']
        collection = my_db.test

        username = self.current_user
        # print(username)
        # print("username: " + username)
        # find him in db
        v1 = await do_find_one(collection, username)
        # pprint.pprint(v1)

        if v1 is not None:

            # izvuci njegove vesti i renderuj ih na stranici
            headlines = v1['headlines']
            # pprint.pprint(headlines)

            await self.render('profile.html', user=self.current_user, headlines=headlines)

        else:
            print('Unknown client.')
        """
        self.render('profile.html', user="")

    async def post(self):
        """
        print('---' * 26)
        dic_data = tornado.escape.json_decode(self.request.body)
        # print(dic_data)
        print('---' * 26)

        my_db = self.settings['db']
        collection = my_db.test

        if 'passOld' in dic_data:
            old_password = dic_data["passOld"]
            new_password1 = dic_data["passNew1"]
            new_password2 = dic_data["passNew2"]

            if new_password1 != new_password2:
                self.write(json.dumps({'sent': 'mismatched'}))
                return

            current_user_data = await do_find_one(collection, self.current_user)
            current_password = current_user_data['password']
            print("Current password: ", current_password)

            if old_password != current_password:
                self.write(json.dumps({'sent': 'current'}))
                return

            val = await do_alter_password(collection, self.current_user, new_password1)
            if val is not None:
                print('Password updated.')
                self.write(json.dumps({'sent': 'changed'}))
                return
            else:
                print('An error occurred while adjusting the timer')
            return

        if 'article' in dic_data:

            username = self.current_user
            headline = dic_data['article']
            id_headline = dic_data['id_article']

            v1 = await do_delete_one(collection, username, headline)
            print("result %s" % repr(v1))
            self.write(json.dumps({'sent': id_headline}))
        """
