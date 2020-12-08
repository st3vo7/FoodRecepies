import sqlite3

DB_NAME = "db.sqlite"


def create_table():
    try:
        conn = sqlite3.connect(DB_NAME)
    except ConnectionRefusedError as e:
        print(e)
        raise
    else:
        conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
                    user_id INTEGER PRIMARY KEY,
                    user_name TEXT,
                    user_surname TEXT,
                    email TEXT
                    )
        """)

        conn.execute("""
        CREATE TABLE IF NOT EXISTS recipes (
                    recipe_id INTEGER PRIMARY KEY,
                    recipe_name TEXT,
                    recipe_text TEXT,
                    rating INTEGER,
                    prep_time INTEGER,
                    persons INTEGER,
                    num_ratings INTEGER
                    )
        """)

        conn.execute("""
        CREATE TABLE IF NOT EXISTS user_recipe (
                    ur_id INTEGER PRIMARY KEY,
                    user_id INTEGER,
                    recipe_id INTEGER,
                    FOREIGN KEY (user_id) REFERENCES users (user_id),
                    FOREIGN KEY (recipe_id) REFERENCES recipes (recipe_id)
                    )
        """)

        conn.execute("""
        CREATE TABLE IF NOT EXISTS ingredients (
                    ingredient_id INTEGER PRIMARY KEY,
                    ingredient_name TEXT UNIQUE,
                    unit TEXT
                    )
        """)

        conn.execute("""
        CREATE TABLE IF NOT EXISTS recipe_ingredient (
                    ri_id INTEGER PRIMARY KEY,
                    recipe_id INTEGER,
                    ingredient_id INTEGER,
                    quantity INTEGER,
                    FOREIGN KEY (recipe_id) REFERENCES recipes (recipe_id),
                    FOREIGN KEY (ingredient_id) REFERENCES ingredients (ingredient_id)
                    )
        """)


def fetch_recipe_id(name, content):
    try:
        conn = sqlite3.connect(DB_NAME)
    except ConnectionRefusedError as e:
        print(e)
    else:
        cur = conn.cursor()
        r = None
        try:
            r = cur.execute("SELECT recipe_id FROM recipes WHERE recipe_name = ? AND recipe_text = ?", (name, content))
            r = r.fetchone()
        except sqlite3.IntegrityError as e:
            print("Trying to write something that already exists in db: ", e)
        conn.commit()
        conn.close()

        return r


def fetch_ingredient_id(ingredient):
    try:
        conn = sqlite3.connect(DB_NAME)
    except ConnectionRefusedError as e:
        print(e)
    else:
        cur = conn.cursor()
        r = None
        try:
            r = cur.execute("SELECT ingredient_id FROM ingredients WHERE ingredient_name = ?", (ingredient, ))
            r = r.fetchone()
        except sqlite3.IntegrityError as e:
            print("Trying to write something that already exists in db: ", e)

        conn.commit()
        conn.close()

        return r


def archive_into_db(name, ingredients, content, preparation, persons):

    li = ingredients.split("\n")

    try:
        conn = sqlite3.connect(DB_NAME)
    except ConnectionRefusedError as e:
        print(e)
    else:
        cur = conn.cursor()
        try:
            cur.execute("INSERT INTO recipes(recipe_name, recipe_text, rating, prep_time, persons, num_ratings) VALUES(?, ?, ?, ?, ?, ?)", (name, content, 0, preparation, int(persons), 0))
        except sqlite3.IntegrityError as e:
            print("Trying to write something that already exists in recipes: ", e)
        else:
            conn.commit()
            conn.close()

        for l1 in li:
            l2 = l1.split(" ")
            ingredient = l2[0]
            q = l2[1]
            u = l2[2]
            try:
                conn = sqlite3.connect(DB_NAME)
            except ConnectionRefusedError as e:
                print(e)
            else:
                cur = conn.cursor()
                try:
                    cur.execute("INSERT INTO ingredients(ingredient_name, unit) VALUES(?, ?)", (ingredient, u))
                except sqlite3.IntegrityError as e:
                    print("Trying to write something that already exists in ingredients: ", e)
                else:
                    conn.commit()
                    conn.close()
                try:
                    r_id = fetch_recipe_id(name, content)
                    r_id = r_id[0]
                    print("r_id: ", r_id)
                    i_id = fetch_ingredient_id(ingredient)
                    print(i_id)
                    i_id = i_id[0]
                    print("i_id: ", i_id)

                    conn = sqlite3.connect(DB_NAME)
                except ConnectionRefusedError as e:
                    print(e)
                else:
                    cur = conn.cursor()
                    try:
                        cur.execute("INSERT INTO recipe_ingredient(recipe_id, ingredient_id, quantity) VALUES(?, ?, ?)", (r_id, i_id, q))
                    except sqlite3.IntegrityError as e:
                        print("Trying to write something that already exists in recipe_ingredient: ", e)
                    else:
                        conn.commit()
                        conn.close()


def get_all_recipes():
    r = None
    try:
        conn = sqlite3.connect(DB_NAME)
    except ConnectionRefusedError as e:
        print(e)
    else:
        cur = conn.cursor()
        try:
            r = cur.execute("SELECT recipe_name, recipe_text, rating, prep_time, persons, num_ratings, recipe_id FROM recipes")
            r = r.fetchall()
        except sqlite3.DatabaseError as e:
            print(e)
        else:
            conn.commit()
            conn.close()
    return r


def get_top_ingredients():
    r = []
    try:
        conn = sqlite3.connect(DB_NAME)
    except ConnectionRefusedError as e:
        print(e)
    else:
        cur = conn.cursor()
        try:
            r = cur.execute("""
                        SELECT i.ingredient_name, COUNT(*) as count FROM ingredients i
                        JOIN recipe_ingredient ri
                        WHERE i.ingredient_id = ri.ingredient_id
                        GROUP BY ri.ingredient_id
                        HAVING count > 0
                        ORDER BY count DESC
                        LIMIT 5
                        """)
            r = r.fetchall()
        except sqlite3.DatabaseError as e:
            print(e)
        else:
            conn.commit()
            conn.close()
    return r


def search_for_name(keywords):
    r = None
    try:
        conn = sqlite3.connect(DB_NAME)
    except ConnectionRefusedError as e:
        print(e)
    else:
        cur = conn.cursor()
        try:
            r = cur.execute("""  
                            SELECT recipe_name, recipe_text, rating, prep_time, persons, num_ratings, recipe_id
                            FROM recipes
                            WHERE recipe_name = ?
                            """, (keywords, ))
            r = r.fetchall()
        except sqlite3.DatabaseError as e:
            print(e)
        else:
            conn.commit()
            conn.close()
    return r


def search_for_ingredients(keywords):
    r = None

    try:
        conn = sqlite3.connect(DB_NAME)
    except ConnectionRefusedError as e:
        print(e)
    else:
        cur = conn.cursor()
        try:
            # works only for one ingredient
            # in order to make it work for multiple recipes, here's general idea
            # look up for all recipe_ids containing just the first ingredient, and store it. Then
            # iterate through list of ingredients [2:] and select recipes id
            # and join with first table of results on recipe_id
            # So, if recipe contains both ingredients it will stay in the table,
            # otherwise, it will not.
            r = cur.execute("""                 
                                SELECT distinct recipe_name, recipe_text, rating, prep_time, persons, num_ratings, r.recipe_id
                                FROM recipes r JOIN recipe_ingredient ri 
                                ON r.recipe_id = ri.recipe_id
                                JOIN ingredients i on i.ingredient_id = ri.ingredient_id 
                                WHERE ingredient_name = ?
                                """, (keywords,))
            r = r.fetchall()
        except sqlite3.DatabaseError as e:
            print(e)
        else:
            conn.commit()
            conn.close()
    return r


def search_for_text(keywords):
    r = None
    try:
        conn = sqlite3.connect(DB_NAME)
    except ConnectionRefusedError as e:
        print(e)
    else:
        cur = conn.cursor()
        try:
            r = cur.execute("""
                                SELECT recipe_name, recipe_text, rating, prep_time, persons, num_ratings, recipe_id
                                FROM recipes
                                WHERE recipe_text = ?
                                """, (keywords,))
            r = r.fetchall()
        except sqlite3.DatabaseError as e:
            print(e)
        else:
            conn.commit()
            conn.close()
    return r


def get_recipe_ingredients(recipe_id):
    # print("u get_recipe_ingredients sam")
    r = []
    try:
        conn = sqlite3.connect(DB_NAME)
    except ConnectionRefusedError as e:
        print(e)
    else:
        cur = conn.cursor()
        try:
            for row in cur.execute("""
                            SELECT ingredient_name, ri.quantity, unit 
                            FROM ingredients i JOIN recipe_ingredient ri
                            ON i.ingredient_id = ri.ingredient_id
                            WHERE ri.recipe_id = ? 
                            """, (recipe_id,)):
                # print("ironed row: ", " ".join(map(str, row)))
                r.append(" ".join(map(str, row)))
            # print(r)
        except sqlite3.DatabaseError as e:
            print(e)
        else:
            conn.commit()
            conn.close()
    return r


def update_rating(new_rating, r_id):
    r = None
    try:
        conn = sqlite3.connect(DB_NAME)
    except ConnectionRefusedError as e:
        print(e)
    else:
        cur = conn.cursor()
        try:
            r = cur.execute("""
                        UPDATE recipes
                        SET rating = rating + ?, num_ratings = num_ratings + 1
                        WHERE recipe_id = ?
                        """, (new_rating, r_id))
            r = r.fetchall()
            # print(r)
        except sqlite3.DatabaseError as e:
            print(e)
        else:
            conn.commit()
            conn.close()
    return r


def count_average(r_id):
    r = None
    try:
        conn = sqlite3.connect(DB_NAME)
    except ConnectionRefusedError as e:
        print(e)
    else:
        cur = conn.cursor()
        try:
            r = cur.execute("""
                            SELECT rating, num_ratings
                            FROM recipes
                            WHERE recipe_id = ?
                            """, (r_id,))
            r = r.fetchall()
        except sqlite3.DatabaseError as e:
            print(e)
        else:
            conn.commit()
            conn.close()
    return r
