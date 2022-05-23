from flask import render_template, redirect, session, request, flash
from flask_app import app 
from flask_app.models.user_model import User
from flask_app.models.movie_model import Movie
from flask_bcrypt import Bcrypt 
bcrypt = Bcrypt (app) 


@app.route('/actors') 
def actor(): 
    if not User.validate_register(request.form):
        return redirect('/') 
    