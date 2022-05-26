# from crypt import methods
from flask_app import app 
from flask_app.models.user_model import User 
from flask_app.models.movie_model import Movie 
from flask_app.models.actor_model import Actor
from flask import render_template, redirect, session, request, flash, url_for
import os
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'C:\\Users\\Alexis\\OneDrive\\Desktop\\group_project_2022\\flask_app\\static\\images'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/actors') 
def actors_page(): 
    if "user_id" not in session:
        return redirect('/') 
    data = { "id" : session ["user_id"]}
    return render_template('add_actor.html', user = User.get_by_id(data)) 


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/create/actors', methods=['GET', 'POST'])
def upload_actor():
    #check if user in session if not kick out
    if "user_id" not in session:



        return redirect('/logout')
    # if doesn't reach validation requiremnts just redirects back to the page it's on
    if request.method == 'POST':
        print("----------------------")
        print(request.form["first_name"])
        print("----------------------")
        if not Actor.validate_actor(request.form):
            return redirect ('/create/actors')   
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part', "actor")
            return redirect('/create/actors') # changed this from /dashboard to this
        file = request.files['file']
        print("*********", file )
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file', "actor")
            return redirect('/create/actors') #changed this from /dashboard to this
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            print(filename)
            data = {
                "first_name" : request.form["first_name"], 
                "last_name" : request.form["last_name"], 
                "img_path" : "/static/images/" + filename,
            }
            actors_id = Actor.create_actor(data)
            many_data = {
                "movie_id" : session["movies_id"],
                "actor_id" : actors_id
            }
            Actor.create_many(many_data)
    # if successful, reaches add actors page to insert 3 actors. 
    return redirect('/dashboard') 
    # in dashboard, maybe create with jinja 

@app.route('/actor/profile/<int:id>') 
def actors_profile_page(id): 
    if "user_id" not in session:
        return redirect('/') 
    data = { "id" : id}
    user_data = {
        "id" : session["user_id"]
    }
    return render_template('actor_profile.html', user = User.get_by_id(user_data), actor = Actor.get_actor_with_movies(data)) 
