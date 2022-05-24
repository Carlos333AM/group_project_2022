from flask_app.config.mysqlconnection import connectToMySQL 


class Actor: 
    db_name = "group_project" 
    
    def __init__(self,data): 
        self.id = data['id'] 
        self.first_name = data['first_name'] 
        self.last_name = data['last_name'] 
        self.img_path = data['img_path'] 
        self.created_at = data['created_at'] 
        self.updated_at = data['updated_at'] 

    # CREATE and SAVE actor into database 
    @classmethod 
    def create_actor(cls,data): 
        query = "INSERT INTO actors (first_name, last_name, img_path) VALUES (%(first_name)s,%(last_name)s,%(img_path)s);" 
        return connectToMySQL(cls.db_name).query_db(query, data) 


    # CREATE and SAVE actor into database 
    # @classmethod 
    # def create_actor(cls,data): 
    #     query = "INSERT INTO actors (first_name, last_name, img_path) VALUES (%(first_name)s,%(last_name)s,%(img_path)s);" 
    #     return connectToMySQL(cls.db_name).query_db(query, data) 



    #RETRIVE ALL actors from database 
    @classmethod
    def get_all_actors(cls):
        query = "SELECT * FROM actors;"
        results = connectToMySQL(cls.db_name).query_db(query) 
        print(results) 
        all_actors = [] 
        for row in results: 
            print(row['first_name']) 
            all_actors.append(cls(row)) 
        return all_actors 

    #RETRIEVE ONE actor from database by movie's id 
    @classmethod
    def get_one_actor(cls,data): 
        query = "SELECT * FROM actors WHERE id = %(id)s;"
        results = connectToMySQL(cls.db_name).query_db(query,data)
        return cls(results[0]) 


    # @classmethod 
    # def get_actor_with_movies(cls,data): 
    #     query = " ;" 
    #     results = connectToMySQL(cls.db_name).query_db(query,data)
    #     return cls(results[0]) 
