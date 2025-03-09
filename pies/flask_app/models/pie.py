from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.user import User
from flask import flash


class Pie:
    DB = "pies"
    def __init__(self,data):
        self.id = data['id']
        self.name = data['name']
        self.filing = data['filing']
        self.crust = data['crust']
        self.user_id = data['user_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.creator = None

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM pies JOIN users ON pies.user_id =users.id;"

        results = connectToMySQL(cls.DB).query_db(query)
        print(results)
        all_pies = []
        for row in results:
            this_pie = Pie(row)
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
            this_pie.creator = (user_data)
            all_pies.append(this_pie)
        return all_pies
    

    @classmethod
    def save(cls,data):
        query= "INSERT INTO pies (name, filing, crust, user_id, created_at, updated_at) VALUES (%(name)s,%(filing)s,%(crust)s, %(user_id)s, NOW(), NOW());"
        return connectToMySQL(cls.DB).query_db(query,data)

    @classmethod
    def update(cls,data):
        query = "UPDATE pies SET name = %(name)s, filing = %(filing)s, crust = %(crust)s, updated_at = NOW() WHERE id = %(id)s"
        return connectToMySQL(cls.DB).query_db(query,data)

    @classmethod
    def delete(cls,data):
        query = "DELETE FROM pies WHERE id = %(id)s"
        return connectToMySQL(cls.DB).query_db(query,data)

    @classmethod
    def get_by_id(cls,data):
        
        query = "SELECT * FROM pies WHERE id = %(id)s"

        result = connectToMySQL(cls.DB).query_db(query,data)
        
    
        # this_recipe.person = person
        return cls(result[0])

    @staticmethod
    def validator(form_data):
        is_valid = True
        if len(form_data['name']) < 3:
            is_valid = False
            flash("Please include the name.", "err_name")
        if len(form_data['filing']) < 3:
            is_valid = False
            flash("Please include the filing.", "err_filing")
        if len(form_data['crust']) < 3:
            is_valid = False
            flash("Please include the crust.", "err_crust")
            
        return is_valid