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
                    persons INTEGER
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
                    ingredient_name TEXT,
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
