from flask_app import app
from flask import render_template, redirect, session, request, flash, url_for
import os
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = '/Users/carlosamezcuajr/Desktop/group_project_2022/flask_app/static/images'
# C:\\Users\\Alexis\\OneDrive\\Desktop\\group_project_2022\\flask_app\\static\\images please do not delete this time. 
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

from flask_app.models.movie_model import Movie 
from flask_app.models.user_model import User 
from flask_app.models.actor_model import Actor 


@app.route('/test')
def test():
    return render_template("test.html")


# Routes to page that shows a form to create a movie 
@app.route('/create/movie')
def create_movie(): 
    if "user_id" not in session: 
        return redirect ('/logout')
    data = { "id" : session ["user_id"]}
    return render_template("create_movie.html", user = User.get_by_id(data))
    #gotta rethink the render_template


#Function and Route to upload movie

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload/movie', methods=['GET', 'POST'])
def upload_file():
    #check if user in session if not kick out
    if "user_id" not in session:
        return redirect('/logout')
    # if doesn't reach validation requiremnts just redirects back to the page it's on
    if not Movie.validate_movie(request.form):
        return redirect ('/create/movie')   
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect('/dashboard') # change this 
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect('/dashboard') #change this
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            print(filename)
            data = {
                "rating" : request.form["rating"], 
                "title" : request.form["title"], 
                "img_path" : "/static/images/" + filename,
                "description" : request.form ["description"], 
                "user_id" : session["user_id"]
            }
            movies_id = Movie.create_movie(data)
            session["movies_id"] = movies_id
        # if successful, reaches add actors page to insert 3 actors. 
        return redirect('/actors') 



#Route that shows a html with a from to edit movie. (edit_movie.html)
@app.route('/edit/movie/<int:id>')
def edit_movie(id):
    if "user_id" not in session: 
        return redirect('/logout')
    data = {
        "id" : id 
    }
    user_data = {
        "id" : session ['user_id']
    }
    return render_template("edit_movie.html", movie = Movie.get_one_movie(data), user = User.get_by_id(user_data))



#Route that POST updated movie
@app.route('/update/movie/<int:id>', methods = ['GET','POST'])
def update_movie(id):
    #check if user in session if not kick out
    if "user_id" not in session:
        return redirect('/logout')
    # if doesn't reach validation requiremnts just redirects back to the page it's on
    if not Movie.validate_movie(request.form):
        return redirect (f'/edit/movie/{id}')   
    if request.method == 'POST':
        # check if the post request has the file part
        movie = Movie.get_one_movie({"id": id})
        print('****************', request.files)
        if 'file' not in request.files:
            flash('No file part')
        file = request.files["file"]
        print(file)
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            print(filename)
            data = {
                "id" : id, 
                "rating" : request.form["rating"], 
                "title" : request.form["title"], 
                "img_path" : "/static/images/" + filename,
                "description" : request.form ["description"], 
                "user_id" : session["user_id"]
            }
            Movie.update_movie(data)
        else: 
            data = {
                "id" : id, 
                "rating" : request.form["rating"], 
                "title" : request.form["title"], 
                "img_path" : movie.img_path, 
                "description" : request.form ["description"], 
                "user_id" : session["user_id"]
            }
            Movie.update_movie(data)
        # if successful reaches dashboard? or new movie profile?
        return redirect('/dashboard') #change this


#Route that goes to singular movie profile - connect to the title of movie 
@app.route('/movie/<int:id>')
def show_movie_profile(id):
    if "user_id" not in session:
        return redirect ('/logout')
    data = {"id" : id }
    user_data = {
        "id" : session["user_id"]
    }
    # comment_data = {
    #     "id" : id
    # As of right now, it is holding same id that is in data (the movie id)
    # }

    return render_template("movie_profile.html", user = User.get_by_id(user_data), movie = Movie.get_movies_with_actor(data))


#Deltes movie by movie id 
@app.route('/destroy/movie/<int:id>')
def destroy_movie(id):
    if "user_id" not in session: 
        return redirect ('/logout')
    data = {
        "id" : id 
    }
    Movie.destroy(data)
    return redirect('/dashboard')


