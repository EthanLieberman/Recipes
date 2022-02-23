from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import MyCustomDB
class Recipe:                         # singular instance of...
    def __init__(self,data):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.instructions = data['instructions']
        self.under30 = data['under30']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.users_id = data['users_id']







    @classmethod
    def new_recipe(cls, data):
        query = "INSERT INTO recipes (name, description, instructions, under30, created_at, updated_at, users_id) VALUES( %(name)s, %(description)s, %(instructions)s, %(under30)s, NOW(), NOW(), %(users_id)s );"

        return connectToMySQL(MyCustomDB).query_db( query, data )


    @classmethod
    def getAll_recipe(cls):
        query = "SELECT * FROM recipes;"
        results = connectToMySQL(MyCustomDB).query_db( query)

        all_recipes = []
    # Iterate over the db results and create instances of users with cls.
        for row in results:
            all_recipes.append( cls(row) )
        return all_recipes


    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM recipes WHERE id = %(id)s ;"
        results = connectToMySQL(MyCustomDB).query_db(query, data)
        return cls(results[0])


    @classmethod
    def update_recipe(cls, data):
        query = "UPDATE recipes SET name = %(name)s, description = %(description)s, instructions = %(instructions)s, under30 = %(under30)s, updated_at = NOW(), users_id = %(users_id)s WHERE id = %(id)s;"
        return connectToMySQL(MyCustomDB).query_db( query, data )


    @classmethod
    def delete_recipe(cls, data):
        query = "DELETE FROM recipes WHERE id = %(id)s"
        return connectToMySQL(MyCustomDB).query_db( query, data )