from flask_app.config.mysqlconnection import MySQLConnection, connectToMySQL
from flask import flash
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class Recipe:
    def __init__(self,data):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.instructions = data['instructions']
        self.recipe_date = data['recipe_date']
        self.time_length = data['time_length']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
    
    @classmethod
    def save_recipe(cls, data):
        query = "INSERT into recipes (name, description, instructions, recipe_date, time_length, user_id, created_at, updated_at) VALUES (%(name)s, %(description)s, %(instructions)s, %(recipe_date)s, %(time_length)s, %(user_id)s, NOW(), NOW())"
        return MySQLConnection('recipes').query_db(query, data)
    
    @staticmethod
    def validate_recipe(form):
        is_valid = True
        if len(form['name']) < 3:
            flash ('Name must be at least 3 characters','new_recipe')
            is_valid = False
        if len(form['description']) < 3:
            flash ('Description must be at least 3 characters','new_recipe')
            is_valid = False
        if len(form['instructions']) < 3:
            flash (' instructions must be at least 3 characters','new_recipe')
            is_valid = False
        if form['recipe_date'] == "":
            flash ('Created date field is required','new_recipe')
            is_valid = False
        return is_valid
    
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM recipes"
        results = connectToMySQL('recipes').query_db(query)
        recipes_all = []
        for r in results:
            recipes_all.append(cls(r))
        print(recipes_all)
        return recipes_all
    
    @classmethod
    def get_one(cls,data):
        query = "SELECT * FROM recipes WHERE id = %(id)s"
        results = MySQLConnection('recipes').query_db(query, data)
        return cls(results[0])
    
    @classmethod
    def update_recipe(cls, data):
        query = "UPDATE recipes SET name=%(name)s, description =%(description)s, instructions =%(instructions)s, recipe_date =%(recipe_date)s, time_length = %(time_length)s, updated_at = NOW() WHERE id = %(id)s; "
        return connectToMySQL('recipes').query_db(query, data)
    
    @classmethod
    def destroy_recipe(cls,data):
        query = "DELETE FROM recipes WHERE id = %(id)s;"
        return connectToMySQL('recipes').query_db(query, data)
