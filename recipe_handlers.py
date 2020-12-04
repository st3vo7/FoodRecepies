from base_handler import *
from db_manipulation import *


class MainHandler(BaseHandler):

    def get(self):

        rx = get_all_recipes()
        ix = get_top_ingredients()

        self.render('homepage.html', recipes=rx, ingredients=ix)
        return

    def post(self):
        r = None
        category = self.get_argument("category", None)
        # print(category)
        keywords = self.get_argument("r_search", None)
        # print(keywords)
        if category == "name":
            r = search_for_name(keywords)
        elif category == "ingredients":
            r = search_for_ingredients(keywords)
        elif category == "text":
            r = search_for_text(keywords)

        # TO-DO: generate page with all of the results
        ix = get_top_ingredients()

        self.render('homepage.html', recipes=r, ingredients=ix)
        return


class ProfileHandler(BaseHandler):

    def prepare(self):
        super().prepare()

    # @tornado.web.authenticated
    def get(self):

        rx = get_all_recipes()
        self.render('profile.html', user="", recipes=rx)

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
