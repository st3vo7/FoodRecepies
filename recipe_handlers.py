from base_handler import *
from db_manipulation import *


class MainHandler(BaseHandler):

    def get(self):

        rx = get_all_recipes()  # recipe_name, recipe_text, rating, prep_time, persons, num_ratings, recipe_id
        ix = get_top_ingredients()

        print("r: ", rx)
        ids = []
        for t in rx:
            ids.append(t[6])
        # print("id-jevi recepata: ", ids)

        r_i = {}

        for id1 in ids:
            r = get_recipe_ingredients(id1)
            r_i[id1] = r
        print("r_i:", r_i)

        self.render('homepage.html', recipes=rx, recipe_ingredients=r_i, ingredients=ix)
        return

    def post(self):
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

        print("rx:", rx)

        ids = []
        if rx is not None:
            for t in rx:
                ids.append(t[6])
        print("id-jevi recepata: ", ids)

        r_i = {}

        for id1 in ids:
            r = get_recipe_ingredients(id1)
            r_i[id1] = r
        print("r_i:", r_i)

        self.render('homepage.html', recipes=rx, recipe_ingredients=r_i, ingredients=ix)
        return


class ProfileHandler(BaseHandler):

    def prepare(self):
        super().prepare()

    # @tornado.web.authenticated
    def get(self):

        rx = get_all_recipes()

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

        self.render('profile.html', user="", recipes=rx, recipe_ingredients=r_i)

    def post(self):
        if self.get_argument("create", None) is not None:
            print("create")
            self.redirect("/create")
            return


class CreateHandler(BaseHandler):

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

        archive_into_db(name, ingredients, content, preparation, persons)

        self.redirect("/profile")
        return
