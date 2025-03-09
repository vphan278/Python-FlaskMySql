from flask_app.config.mysqlconnection import connectToMySQL

class Ninja:
    DB = "dojos_a_ninjas"
    def __init__( self, data ):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.age = data['age']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']


    @classmethod
    def save_ninja(cls, data):      # create a new Ninja and save to specific dojo (in ninjas page)
        query = """
                INSERT INTO ninjas ( first_name, last_name, age, dojo_id, created_at, updated_at ) 
                VALUES (%(first_name)s, %(last_name)s, %(age)s, %(dojo_id)s, NOW(), NOW() );
                """
        results = connectToMySQL(cls.DB).query_db(query, data)
        return results
#############################################################33
    
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM ninjas;"
        # make sure to call the connect_to_mysql function with the schema you are targeting.
        results = connectToMySQL(cls.DB).query_db(query)
        # Create an empty list to append our instances of friends
        ninjas = []
        # Iterate over the db results and create instances of friends with cls.
        for ninja in results:
            ninjas.append(cls(ninja))
        return ninjas

    @classmethod
    def get_one(cls, ninja_id):
        query  = "SELECT * FROM ninjas WHERE id = %(id)s;"
        data = {'id': ninja_id}
        results = connectToMySQL(cls.DB).query_db(query, data)
        return cls(results[0])

            

    #@classmethod
    #def save(cls, data):
    #    query = "INSERT INTO friends (first_name, last_name, occupation, created_at, updated_at) VALUES (%(fname)s, %(lname)s, %(occ)s, NOW(), NOW());"
        # data is a dictionary that will be passed into the save method from server.py
    #    return connect_to_mysql('first_flask').query_db(query, data)



    @classmethod
    def delete(cls, ninja_id):
        query = "DELETE FROM ninjas WHERE id = %(id)s;"
        data = {"id": ninja_id}
        return connectToMySQL(cls.DB).query_db(query, data)

        
    @classmethod
    def update(cls, data):
        query = """UPDATE ninjas SET first_name=%(first_name)s, last_name=%(last_name)s, age=%(age)s, created_at=NOW(), 
        updated_at = NOW() WHERE id = %(id)s """

        return connectToMySQL(cls.DB).query_db(query, data)

    



    

