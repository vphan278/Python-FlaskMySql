# Import mysqlconnection config
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re # The regex module

from flask_app import app
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)


"""
Import other models files for access to classes.
We import the file rather than the class to avoid circular import
Example: from flask_app.controllers import ninja 
"""

# Regular expression for email validation
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
password_pattern = "^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$"


class User:
    DB = "recipes"
    def __init__(self, data):
        """Model a user"""
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def create_user(cls, data):
        """Add new user to db"""
        query = "INSERT INTO users (first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);"
        return connectToMySQL(cls.DB).query_db(query,data)
        
    @classmethod
    def get_user_by_id(cls, data):
        """Get the user by id"""
        query = "SELECT * FROM users WHERE id = %(id)s;"
        # Returns list & we make an instance of the first index of that list
        return cls(connectToMySQL(cls.DB).query_db(query, data)[0])

    @classmethod
    def get_user_by_email(cls, data):
        """Get user by email"""
        query = "SELECT * FROM users WHERE email = %(email)s;"
        # Returns list & we make an instance of the first index of that list
        result = connectToMySQL(cls.DB).query_db(query, data)
        # Check for a result
        if len(result) < 1:
            return False
        return cls(result[0])


    @staticmethod
    def validate_registration(user):
            """Validate the add a user form"""
            is_valid = True # We assume this is true
            if len(user['first_name']) < 2:
                flash("The first name must be at least 2 characters.", "danger")
                is_valid = False
            if len(user['last_name']) < 2:
                flash("The last name must be at least 2 characters.", "danger")
                is_valid = False
            # Validate email
            if len(user['email']) < 3:
                flash("The email must be at least 3 characters.", "danger")
                is_valid = False
            # Check for if email has already been used and stored in db
            query = "SELECT * FROM users WHERE email = %(email)s;"
            data = {
                "email": user['email']
            }
            email_result = connectToMySQL('recipes').query_db(query, data)
            # Check to see if the query returned an result with that email;
            # if yes return False
            if len(email_result) >= 1:
                flash("Email is already used. Please sign in or register with different email.", "danger")
                is_valid = False
                return is_valid
            # Test whether a field matches the pattern
            if not EMAIL_REGEX.match(user['email']):
                flash("Email is not valid!", "danger")
                is_valid = False
                return is_valid
            if len(user['password']) < 3:
                flash("The password must be at least 8 characters, and contain at least one each of the following: one upper, one lower, one digit and one special character.", "danger")
                is_valid = False
            if not re.match(password_pattern, user['password']):
                flash("The password must be at least 8 characters, and contain at least one each of the following: one upper, one lower, one digit and one special character.", "danger")
                is_valid = False

            if user["password"] != user["confirm_password"]:
                flash("Password don't match")
                is_valid = False

            return is_valid

    ####################################################################################################

    