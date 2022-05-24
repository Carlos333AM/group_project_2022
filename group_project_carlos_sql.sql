use group_project; 


SELECT * FROM users; 
SELECT * FROM users WHERE id = 1; 


SELECT * FROM movies; 
SELECT * FROM movies WHERE id = 1; 

SELECT * FROM comments; 

SELECT * FROM actors_has_movies; 

SELECT * FROM users WHERE email = %(email)s;


SELECT * FROM actors; 