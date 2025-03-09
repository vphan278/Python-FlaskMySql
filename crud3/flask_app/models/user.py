# import the function that will return an instance of a connection
from flask_app.config.mysqlconnection import connect_to_mysql
# model the class after the friend table from our database

class User:
    DB = "crud3"
    def __init__( self , data ):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
    # Now we use class methods to query our database
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"
        # make sure to call the connect_to_mysql function with the schema you are targeting.
        results = connect_to_mysql('crud3').query_db(query)
        # Create an empty list to append our instances of friends
        users = []
        # Iterate over the db results and create instances of friends with cls.
        for user in results:
            users.append(cls(user))
        return users

    @classmethod
    def get_one(cls, user_id):
        query  = "SELECT * FROM users WHERE id = %(id)s;"
        data = {'id': user_id}
        results = connect_to_mysql(cls.DB).query_db(query, data)
        return cls(results[0])

            

    @classmethod
    def save(cls, data):
        query = "INSERT INTO users (first_name, last_name, email, created_at, updated_at) VALUES (%(fname)s, %(lname)s, %(email)s, NOW(), NOW());"
        # data is a dictionary that will be passed into the save method from server.py
        return connect_to_mysql('crud3').query_db(query, data)

    @classmethod
    def delete(cls, user_id):
        query = "DELETE FROM users WHERE id = %(id)s;"
        data = {"id": user_id}
        return connect_to_mysql(cls.DB).query_db(query, data)



    @classmethod
    def update(cls, data):
        query = """UPDATE users SET first_name=%(first_name)s, last_name=%(last_name)s, email=%(email)s, created_at=NOW(), 
        updated_at = NOW() WHERE id = %(id)s """

        return connect_to_mysql(cls.DB).query_db(query, data)

    

