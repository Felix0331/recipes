from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re	# the regex module
from flask_bcrypt import Bcrypt
from flask_app import app      
bcrypt = Bcrypt(app) 

class Recipe:
    def __init__( self , data ):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.instructions = data['instructions']
        self.date_made = data['date_made']
        self.under_30_minutes = data['under_30_minutes']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
    
    @classmethod
    def add_recipe( cls , data ):
        query = "INSERT INTO recipes ( name , description ,instructions, date_made, under_30_minutes, created_at , updated_at, user_id ) VALUES (%(name)s,%(description)s,%(instructions)s,%(date_made)s, %(under_30_minutes)s, NOW(),NOW(), %(user_id)s);"
        return connectToMySQL('recipes_schema').query_db(query,data)    

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM recipes;"
        results = connectToMySQL('recipes_schema').query_db(query)
        recipes = []
        for recipe in results:
            recipes.append( cls(recipe) )
        return recipes

    @classmethod
    def get_recipe(cls,data):
        query = "SELECT * FROM recipes WHERE recipes.id = %(id)s;"
        return connectToMySQL('recipes_schema').query_db(query,data)

    @classmethod
    def edit_recipe( cls , data ):
        query = "UPDATE  recipes SET  name = %(name)s, description = %(description)s ,instructions = %(instructions)s, date_made = %(date_made)s, under_30_minutes = %(under_30_minutes)s, updated_at = NOW(), user_id = %(user_id)s WHERE recipes.id = %(id)s;"
        return connectToMySQL('recipes_schema').query_db(query,data)  

    @classmethod
    def delete_recipe(cls,data):
        query = "DELETE FROM recipes WHERE recipes.id = %(id)s;"
        return connectToMySQL('recipes_schema').query_db(query,data)  
