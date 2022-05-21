from flask_app import app
from flask import render_template, redirect, session, request, flash, url_for
import os
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = '/Users/mikaylathomas/Desktop/group_project_2022/flask_app/static/images'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

from flask_app.models.movie_model import Movie 
from flask_app.models.user_model import User 




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
            Movie.create_movie(data)
        # if successful reaches dashboard? or new movie profile?
        return redirect('/dashboard') #change this



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

#Route that posts updated movie
@app.route('/update/movie', methods = ['POST']) #<int:movie_id>
def update_movie():
    if "user_id" not in session: 
        return redirect ('/logout')
    if not Movie.validate_movie(request.form):
        #if doesn't meet validation requirements... where should we go??
        return redirect('create/movie') #f string?? - edit/movie route 
    data = {
        "rating": request.form["rating"], 
        "title" : request.form ["title"],
        "img_path" : request.form ["img_path"],
        "description" : request.form ["description"],
        "id" : request.form ["id"]
    }
    Movie.update_movie(data)
    return redirect ('/dashboard')


#Route that goes to singular movie profile - connect to the title of movie 
@app.route('/movie/<int:id>')
def show_movie_profile(id):
    if "user_id" not in session:
        return redirect ('/logout')
    data = {"id" : id }
    user_data = {
        "id" : session["user_id"]
    }
    return render_template("movie_profile.html", movie = Movie.get_one_movie(data), user = User.get_by_id(user_data))


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



    
    
    
# Route that posts new movie. 
# @app.route('/add/movie', methods = ['POST'])
# def add_movie(): 
#     if 'user_id' not in session:
#         return redirect('/logout')
#     if doesn't reach validation requiremnts just redirects back to the page it's on
#     if not Movie.validate_movie(request.form):
#         return redirect ('/create/movie') 
#     data = {
#         "rating" : request.form["rating"], 
#         "title" : request.form["title"], 
#         "img_path" : request.form ["img_path"], 
#         "description" : request.form ["description"], 
#         "user_id" : session["user_id"]
#     }
#     Movie.create_movie(data)
#     if successful reaches dashboard? or new movie profile?
#     return redirect ('/dashboard')