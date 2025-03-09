from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.user import User
from flask import flash


class Sasquatch:
    DB = "sasquatch"
    def __init__(self,data):
        self.id = data['id']
        self.location = data['location']
        self.date = data['date']
        self.number = data['number']
        self.happened = data['happened']
        
        self.user_id = data['user_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.creator = None

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM sasquatches JOIN users ON sasquatches.user_id =users.id;"

        results = connectToMySQL(cls.DB).query_db(query)
        print(results)
        all_sasquatches = []
        for row in results:
            this_sasquatch = Sasquatch(row)
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
            this_sasquatch.creator = (user_data)
            all_sasquatches.append(this_sasquatch)
        return all_sasquatches

    @classmethod
    def get_by_id(cls,data):
        
        query = "SELECT * FROM sasquatches WHERE id = %(id)s"

        result = connectToMySQL(cls.DB).query_db(query,data)
        
    
        # this_recipe.person = person
        return cls(result[0])

    

    @classmethod
    def save(cls,data):
        query= "INSERT INTO sasquatches (location, number, happened, date, user_id, created_at, updated_at) VALUES (%(location)s,%(number)s,%(happened)s, %(date)s, %(user_id)s, NOW(), NOW());"
        return connectToMySQL(cls.DB).query_db(query,data)

    @classmethod
    def update(cls,data):
        query = "UPDATE sasquatches SET location = %(location)s, number = %(number)s, happened = %(happened)s, date = %(date)s,updated_at = NOW() WHERE id = %(id)s"
        return connectToMySQL(cls.DB).query_db(query,data)

    @classmethod
    def delete(cls,data):
        query = "DELETE FROM sasquatches WHERE id = %(id)s"
        return connectToMySQL(cls.DB).query_db(query,data)


    @staticmethod
    def validator(form_data):
        is_valid = True
        if len(form_data['location']) < 3:
            is_valid = False
            flash("Name must be at least 3 characters long", "err_location")
        if len(form_data['number']) < 3:
            is_valid = False
            flash("Number must be at least 3 characters long", "err_number")
        if len(form_data['happened']) < 3:
            is_valid = False
            flash("What happened must be at least 3 characters long", "err_happened")
        if len(form_data['date']) < 1:
            is_valid = False
            flash("Date field is required", "err_date")

        return is_valid