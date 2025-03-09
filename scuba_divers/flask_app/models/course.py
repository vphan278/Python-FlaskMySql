from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import diver


class Courses:
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.divers = []

    db = 'scuba_diving_school'

    @classmethod
    def get_all_courses(cls):
        query = "SELECT * FROM courses;"
        result = connectToMySQL(cls.db).query_db(query)
        return result
    
    @classmethod
    def insert_courses(cls, data):
        query = "INSERT INTO courses (name, created_at, updated_at) VALUES (%(name)s, NOW(), NOW());"
        result = connectToMySQL(cls.db).query_db(query, data)
        return result
    
    @classmethod
    def get_one_with_divers(cls, data):
        id = {
        "id": data
    }
        query = """
                SELECT * FROM courses 
                LEFT JOIN divers on courses.id = divers.course_id 
                WHERE courses.id = %(id)s;
                """
        result = connectToMySQL(cls.db).query_db(query, id)
        print(result)
      
        course = cls(result[0])
        print(vars(course))
        
        for row in result:
            diver_info = {
                'id': row['divers.id'],
                'first_name': row['first_name'],
                'last_name': row['last_name'],
                'email': row['email'],
                'course_id': row['course_id'],
                'created_at': row['created_at'],
                'updated_at': row['divers.updated_at']
            }
            course.divers.append(diver.Diver(diver_info))
        return course