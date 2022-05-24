from crypt import methods
from flask_app import app 
from flask_app.models.user_model import User 
from flask_app.models.movie_model import Movie 
from flask_app.models.actor_model import Actor
from flask import render_template, redirect, session, request, flash, url_for
import os
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = '/Users/carlosamezcuajr/Desktop/group_project_2022/flask_app/static/images'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/actors') 
def actors_page(): 
    if "user_id" not in session:
        return redirect('/') 
    return render_template('add_actor.html') 

@app.route('/create/actors', methods = ['POST']) 
def actor(): 
    if "user_id" not in session:
        return redirect('/') 
    data ={ 
            "first_name": request.form['first_name'],
            "last_name": request.form['last_name'],
            "img_path": request.form['img_path'] 
    }
    id = Actor.create_actor(data) 
    session['user_id'] = id
    return redirect('/movie_profile') 
