from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.user import User
from flask import flash


class Recipe:
    DB = "recipes"
    def __init__(self,data):
        self.id = data['id']
        self.name = data['name']
        self.under = data['under']
        self.description = data['description']
        self.instructions = data['instructions']
        self.date = data['date']
        self.user_id = data['user_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.creator = None

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM recipes JOIN users ON recipes.user_id =users.id;"

        results = connectToMySQL(cls.DB).query_db(query)
        print(results)
        all_recipes = []
        for row in results:
            this_recipe = Recipe(row)
            user_data = {
                #**row,
                'id': row['users.id'],
                'first_name': row["first_name"],
                'last_name': row["last_name"],
                'email' : row["email"],
                'password': "",
                'created_at':row['users.created_at'],
                'updated_at': row['users.updated_at']
            }
            #this_user = User(user_data)
            this_recipe.creator = (user_data)
            all_recipes.append(this_recipe)
        return all_recipes
    

    @classmethod
    def save(cls,data):
        query= "INSERT INTO recipes (name, under, description, instructions, date, user_id, created_at, updated_at) VALUES (%(name)s,%(under)s,%(description)s,%(instructions)s, %(date)s, %(user_id)s, NOW(), NOW());"
        return connectToMySQL(cls.DB).query_db(query,data)

    @classmethod
    def update(cls,data):
        query = "UPDATE recipes SET name = %(name)s, under = %(under)s, description = %(description)s, instructions = %(instructions)s, date = %(date)s,updated_at = NOW() WHERE id = %(id)s"
        return connectToMySQL(cls.DB).query_db(query,data)

    @classmethod
    def delete(cls,data):
        query = "DELETE FROM recipes WHERE id = %(id)s"
        return connectToMySQL(cls.DB).query_db(query,data)

    @classmethod
    def get_by_id(cls,data):
        
        query = "SELECT * FROM recipes WHERE id = %(id)s"

        result = connectToMySQL(cls.DB).query_db(query,data)
        
    
        # this_recipe.person = person
        return cls(result[0])

    @staticmethod
    def validator(form_data):
        is_valid = True
        if len(form_data['name']) < 3:
            is_valid = False
            flash("Name must be at least 3 characters long", "err_name")
        if len(form_data['description']) < 3:
            is_valid = False
            flash("Description must be at least 3 characters long", "err_description")
        if len(form_data['instructions']) < 3:
            is_valid = False
            flash("Instructions must be at least 3 characters long", "err_instructions")
        if len(form_data['date']) < 1:
            is_valid = False
            flash("Date field is required", "err_date")
        if "under" not in form_data:
            is_valid = False
            flash("Under 30 minutes field is required", "err_under")
        return is_valid