from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import user_model 

class Movie:
    db_name = "group_project"
    
    def __init__(self,data): 
        self.id = data['id']
        self.rating = data['rating']
        self.title = data['title']
        self.img_path = data['img_path']
        self.description = data['description']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        
    # CREATE and SAVE movie into database
    @classmethod
    def create_movie(cls,data):
        query = "INSERT INTO movies (rating, title, img_path, description, user_id) VALUES (%(rating)s,%(title)s,%(img_path)s, %(description)s,%(user_id)s);"
        return connectToMySQL(cls.db_name).query_db(query, data)
    
        
    #RETRIVE ALL movies from database
    @classmethod
    def get_all_movies(cls):
        query = "SELECT * FROM movies;"
        results = connectToMySQL(cls.db_name).query_db(query)
        print(results)
        all_movies = []
        for row in results: 
            print(row['title'])
            all_movies.append(cls(row))
        return all_movies
            #bring comments into this class method
    
    #RETRIEVE ONE movie from database by movie's id 
    @classmethod
    def get_one_movie(cls,data): 
        query = "SELECT * FROM movies WHERE id = %(id)s;"
        results = connectToMySQL(cls.db_name).query_db(query,data)
        return cls(results[0])
    
    #EDIT(Update) movie by movie's id
    @classmethod
    def update_movie(cls,data):
        query = "UPDATE movies SET rating = %(rating)s, title = %(title)s, img_path = %(img_path)s, description = %(description)s WHERE id = %(id)s"
        return connectToMySQL(cls.db_name).query_db(query,data)
    
    #DELETE movie by movie's id 
    @classmethod
    def destroy(cls,data): 
        query = "DELETE FROM movies WHERE id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query,data)
    
    #VALIDATE movie
    @staticmethod
    def validate_movie(movie):
        is_valid = True
        if (movie['rating']) == "":
            is_valid = False
            flash("Please rate this movie","movie")
        if len(movie['title']) < 2:
            is_valid = False
            flash("Title must be at least 2 characters","movie")
        if len(movie['description']) < 3:
            is_valid = False
            flash("Description must be at least 3 characters","movie")
        return is_valid
        