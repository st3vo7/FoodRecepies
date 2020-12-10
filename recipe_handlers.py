from base_handler import *
from db_manipulation import *

import json
import datetime
import pprint
import requests
import tornado.escape
import tornado.web


def additional_info(email):
    url = 'https://person-stream.clearbit.com/v2/combined/find?email=' + email
    r = requests.get(url)
    pprint.pprint(r.json())
    return r.json()


def examine_user_email(email):
    url = 'https://api.hunter.io/v2/email-verifier?email='+email+'&api_key='+API_KEY
    r = requests.get(url)
    pprint.pprint(r.json())
    # print(r.json()['data']['status'])
    return r.json()['data']['status']


class MainHandler(BaseHandler):

    def prepare(self):
        super().prepare()

    def get(self):

        user_id = 0
        user = self.get_current_user()
        # print("user: ", user)
        if user is not None:
            user_id = int(user['user_id'])

        rx = get_all_recipes(user_id)  # recipe_name, recipe_text, rating, prep_time, persons, num_ratings, recipe_id
        ix = get_top_ingredients()
        mx = get_minmax_recipes()  # recipe_id, recipe_name, count(*)
        # print("mx: ", mx)

        # print("r: ", rx)
        ids = []
        for t in rx:
            ids.append(t[6])
        # print("id-jevi recepata: ", ids)

        r_i = {}

        for id1 in ids:
            r = get_recipe_ingredients(id1)
            r_i[id1] = r
        # print("r_i:", r_i)

        self.render('homepage.html', recipes=rx, recipe_ingredients=r_i, ingredients=ix, tops=mx)
        return

    def post(self):

        if self.get_argument("category", None) or self.get_argument("r_search", None):
            rx = []
            category = self.get_argument("category", None)
            # print(category)
            keywords = self.get_argument("r_search", None)
            # print(keywords)
            if category == "name":
                rx = search_for_name(keywords)
            elif category == "ingredients":
                rx = search_for_ingredients(keywords)
            elif category == "text":
                rx = search_for_text(keywords)

            # TO-DO: generate page with all of the results
            ix = get_top_ingredients()

            mx = get_minmax_recipes()
            # print("rx:", rx)

            ids = []
            if rx is not None:
                for t in rx:
                    ids.append(t[6])
            # print("id-jevi recepata: ", ids)

            r_i = {}

            for id1 in ids:
                r = get_recipe_ingredients(id1)
                r_i[id1] = r
            # print("r_i:", r_i)

            self.render('homepage.html', recipes=rx, recipe_ingredients=r_i, ingredients=ix, tops=mx)
            return

        elif tornado.escape.json_decode(self.request.body):
            dic_data = tornado.escape.json_decode(self.request.body)
            # print(int(dic_data['rating']), int(dic_data['identifier'][-1]))
            r = update_rating(int(dic_data['rating']), int(dic_data['identifier'][-1]))
            if r is not None:
                a = count_average(int(dic_data['identifier'][-1]))
                # print(a)
                av = round(a[0][0]/(a[0][1]*1.0), 2)
                self.write(json.dumps({'identifier': dic_data['identifier'], 'avg_rating': av}))
            else:
                self.write(json.dumps(None))


class ProfileHandler(BaseHandler):

    def prepare(self):
        super().prepare()

    @tornado.web.authenticated
    def get(self):

        user = self.get_current_user()
        # print("user: ", user)
        user_id = int(user['user_id'])

        rx = get_my_recipes(user_id)

        # print(rx)
        ids = []
        for t in rx:
            ids.append(t[6])
        # print("id-jevi recepata: ", ids)

        r_i = {}

        for id1 in ids:
            r = get_recipe_ingredients(id1)
            r_i[id1] = r
        print("r_i:", r_i)

        user = self.get_current_user()
        print("user: ", user)

        username = get_name_from_id(int(user['user_id']))[0][0]
        self.render('profile.html', user=username, recipes=rx, recipe_ingredients=r_i)

    def post(self):
        if self.get_argument("create", None) is not None:
            print("create")
            self.redirect("/create")
            return


class CreateHandler(BaseHandler):

    def prepare(self):
        super().prepare()

    def get(self):
        self.render('create.html')

    def post(self):
        # print("detected post")
        name = None
        ingredients = None
        content = None
        persons = None
        preparation = None

        if self.get_body_argument("name", None) is not None:
            name = self.get_body_argument("name")
        if self.get_body_argument("ingredients", None) is not None:
            ingredients = self.get_body_argument("ingredients")
        if self.get_body_argument("content", None) is not None:
            content = self.get_body_argument("content")
        if self.get_body_argument("preparation", None) is not None:
            preparation = self.get_body_argument("preparation")
        if self.get_body_argument("persons", None) is not None:
            persons = self.get_body_argument("persons")

        # print(name)
        # print(ingredients)
        # print(content)
        # print(preparation)
        # print(persons)

        user = self.get_current_user()
        # print("user: ", user)
        user_id = int(user['user_id'])

        archive_into_db(name, ingredients, content, preparation, persons, user_id)

        self.redirect("/profile")
        return


class LoginHandler(BaseHandler):
    def get(self):
        self.render('login.html')

    def post(self):

        user_name = self.get_argument("username", None)
        print("user_name", user_name)
        user_surname = self.get_argument("usersurname", None)
        print("user_surname", user_surname)
        email = self.get_argument("email", None)
        print("email", email)
        password = self.get_argument("password", None)
        print("password", password)

        registered = check_for_user(email)
        print("registered: ", registered)

        if not registered:

            """ HUNTER """
            v = examine_user_email(email)
            if v == 'invalid':
                self.write('<h3>Email invalid. Can not receive messages.</h3>')
                return

            register_user(user_name, user_surname, email, password)

        else:
            p = registered[0][3]
            print("p: ", p)
            if p != password:
                self.write('<h3>Wrong credentials</h3>')
                return

        """Look for additional information about registered user - CLEARBIT"""
        # TODO: REGISTER ON clearbit.com - require info
        """
        ai = additional_info(email)
        location = ai['person']['location']
        print('location: ', location)
        """

        # print("check_for_user(email)[0][0]: ", (check_for_user(email))[0][0])
        self.set_secure_cookie("user_id", str((check_for_user(email))[0][0]))

        token = jwt.encode({'user_name': user_name, 'user_id': str((check_for_user(email))[0][0]), 'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)},
                           SECRET_KEY)
        # print("token.decoded: ", json.dumps({'token': token.decode('UTF-8')}))
        self.set_secure_cookie("token", token.decode('UTF-8'))
        self.redirect('/profile')
