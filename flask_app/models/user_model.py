from flask_app.config.mysqlconnection import connectToMySQL
import re

from flask import flash
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


class Registration:
    db = 'login_and_registration'
    def __init__(self, ninja):
        self.id = ninja['id']
        self.first_name = ninja['first_name']
        self.last_name = ninja['last_name']
        self.email = ninja['email']
        self.password = ninja['password']
        self.created_at = ninja['created_at']
        self.updated_at = ninja['updated_at']
        
    
    
    @classmethod
    def save(cls,data):
        query = """INSERT INTO registrations (first_name, last_name, email, password) 
                VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);"""
        return connectToMySQL(cls.db).query_db(query, data)
    

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM registrations;"
        results = connectToMySQL(cls.db).query_db(query)
        ninja = []
        for row in results:
            ninja.append(cls(row))
        print(results)
        return ninja
    
    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM registrations WHERE email = %(email)s;"
        results = connectToMySQL(cls.db).query_db(query, data)
        
        if len(results) < 1:
            return False
        return cls(results[0])
    
    @classmethod
    def get_by_login_id(cls,data):
        query = "SELECT * FROM registrations WHERE id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query, data)
    
        return cls(results[0])
    
    
    
        
    
    @staticmethod
    def validate_registration(ninja):
        is_valid = True
        query = "SELECT * FROM registrations WHERE email = %(email)s;"
        results = connectToMySQL(Registration.db).query_db(query, ninja)
    
        if len(results) >= 1:
            flash("Email taken", "register") 
            is_valid = False
        if not EMAIL_REGEX.match(ninja['email']): 
            flash("Invalid email address!", "register")
            is_valid = False
        if len(ninja['first_name']) < 3:
            flash("first_name must be at least 3 characters", "register")
            is_valid = False
        if len(ninja['last_name']) < 3:
            flash("last_name must be at least 3 characters", "register")
            is_valid = False
        if  len(ninja['email']) < 3:
            flash("email must be at least 3 characters", "register")
            is_valid = False
        if len(ninja['password']) < 8:
            flash("Password must be at least 8 characters", "register")
            is_valid = False# test whether a field matches the pattern
        if ninja['password'] != ninja['confirm_password']:
            flash("Passwords don't match", "register")
            is_valid = False

        return is_valid