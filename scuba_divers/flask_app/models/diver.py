from flask_app.config.mysqlconnection import connectToMySQL

class Diver:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.course_id = data['course_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    db = "scuba_diving_school"

    @classmethod
    def get_all_divers(cls):
        query = "SELECT * FROM divers;"
        results = connectToMySQL(cls.db).query_db(query)
        divers = []
        for u in results:
            divers.append( cls(u) )
        return divers

    @classmethod
    def update_diver(cls, data):
        query = "UPDATE divers SET first_name = %(first_name)s, last_name = %(last_name)s, email = %(email)s, course_id = %(course_id)s, updated_at = NOW() WHERE id = %(id)s;"
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def get_diver_by_id(cls, id):
        query = "SELECT * FROM divers WHERE id=%(id)s;"
        results = connectToMySQL(cls.db).query_db(query, {"id":id})
        return cls(results[0])
    
    @classmethod
    def insert_diver(cls, data):
        query = "INSERT INTO divers (first_name, last_name, email, course_id, created_at, updated_at) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(course_id)s, NOW(), NOW());"
        return connectToMySQL(cls.db).query_db(query,data) 
    
    @classmethod
    def delete_diver(cls, id):
        query = "DELETE FROM divers WHERE id = %(id)s"
        return connectToMySQL(cls.db).query_db(query,{"id":id})
    