from flask import render_template, redirect, session, request, flash, request
from flask_app import app 
from flask_app.models.comment_model import Comment 
from flask_app.models.movie_model import Movie
from flask_app.models.user_model import User 


@app.route('/add/comment', methods =['POST'])
def add_comment(): 
    if 'user_id' not in session:
        return redirect('/logout')
    comment_data = {
        "content" : request.form["content"],
        "user_id" : session["user_id"],
        "movie_id" : request.form["movie_id"] #ERROR
    }
    user_data = {
        "id": session ['user_id']
    }
    
    Comment.save(comment_data)
    # User.save(user_data)
    return redirect (request.referrer)
    # return render_template('dashboard.html', comment = Comment.post_with_comment(comment_data))


@app.route('/destroy/comment/<int:id>')
def destroy_comment(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":id
    }
    Comment.destroy(data)
    return redirect(request.referrer)