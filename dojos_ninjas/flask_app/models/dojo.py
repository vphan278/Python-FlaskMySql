from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import ninja

class Dojo:
    DB = "dojos_a_ninjas"
    def __init__( self , data ):
        self.id = data['id']
        self.name = data['name']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.ninjas = []

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM dojos"
        dict_of_dojos = connectToMySQL(cls.DB).query_db(query)
        dojos = []
        for one_dojo in dict_of_dojos:
            dojos.append(cls(one_dojo))
        return dojos

    @classmethod
    def get_one(cls, id):           # UNITE ALL THE NINJAS DATA INTO 1 DOJO
        query = """
                SELECT * FROM dojos
                WHERE id = %(id)s;
                """
        results = connectToMySQL(cls.DB).query_db(query, {"id":id})
        return cls(results[0])

    @classmethod        # @classmethod    create/save new dojo (show in default page)
    def save_dojo(cls, data):                   # tested this query = SET @nextID = (SELECT MAX(id) + 1 FROM dojos_and_ninjas.dojos);
        query = """
                INSERT INTO dojos(name, created_at, updated_at) 
                VALUES( %(name)s, NOW(), NOW() );
        """
        return connectToMySQL(cls.DB).query_db(query, data)

    @classmethod
    def one_dojo_with_ninjas(cls, id):
        # query = """ SELECT * FROM dojos LEFT JOIN ninjas ON ninjas.dojo_id = dojos.id WHERE dojos.id = %(id)s; """
        query = """
                SELECT 
                ninjas.id as "ninjas.id", first_name as "ninjas.first_name", 
                last_name as "ninjas.last_name", 
                age as "ninjas.age", dojo_id, ninjas.created_at as "ninjas.created_at", 
                ninjas.updated_at as "ninjas.updated_at", name, dojos.id, dojos.created_at, dojos.updated_at
                FROM dojos
                LEFT JOIN ninjas
                ON ninjas.dojo_id = dojos.id
                WHERE dojos.id = %(id)s;
        """
        results = connectToMySQL('dojos_a_ninjas').query_db(query, {"id":id})
        print(results)
        results_object = cls(results[0])
        for row_from_db in results:
            # Now we parse the ninja data to make instances of ninja and add them into our list.
            ninja_data = {
                "id": row_from_db["ninjas.id"],
                "first_name": row_from_db["ninjas.first_name"],
                "last_name": row_from_db["ninjas.last_name"],
                "age": row_from_db["ninjas.age"],
                "created_at": row_from_db["ninjas.created_at"],
                "updated_at": row_from_db["ninjas.updated_at"]
            }
            results_object.ninjas.append(ninja.Ninja(ninja_data))
        print(results_object.ninjas[0])
        return results_object