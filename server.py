"""Server for movie ratings app."""

from flask import Flask, render_template, request, flash, session, redirect, url_for

from model import connect_to_db, db

import crud

from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = "secreto"
app.jinja_env.undefined = StrictUndefined

# Replace this with routes and view functions!

@app.route("/")
def homepage():
    return render_template("homepage.html")

@app.route("/movies")
def all_movies():
    movies = crud.get_movies()

    return render_template("all_movies.html", movies = movies)

@app.route("/movies/<movie_id>")
def show_movie(movie_id):
    movie = crud.get_movie_by_id(movie_id)
    return render_template("movie_details.html", movie=movie)

@app.route("/users", methods=["GET"])
def all_users():
    
    users = crud.get_users()

    return render_template("all_users.html", users=users)

@app.route("/users", methods=["POST"])
def register_user():

    new_email = request.form["email"]
    new_password = request.form["password"]

    user = crud.get_user_by_email(new_email)
    if user:
        flash("User already exists")
    else:
        new_user = crud.create_user(new_email, new_password)
        db.session.add(new_user)
        db.session.commit()
        flash("User created successfully")

    return redirect("/")

@app.route("/users/<user_id>")
def show_user(user_id):

    user = crud.get_user_by_id(user_id)

    return render_template("user_details.html", user=user)

@app.route("/login", methods=["POST"])
def login():
    email = request.form["email"]
    password = request.form["password"]

    user = crud.get_user_by_email(email)

    if user:
       session["user_email"] = user.email
       flash(f"Successfully logged in as {user.email}")
    else:
        flash("This email is not registered")

    return redirect("/")

@app.route("/rating/<movie_id>", methods=["POST"])
def rate_movie(movie_id):
    user = crud.get_user_by_email(session["user_email"])
    movie = crud.get_movie_by_id(movie_id)

    score = int(request.form["rating"])

    new_rating = crud.create_rating(user, movie, score)
    db.session.add(new_rating)
    db.session.commit()

    return redirect(f"/movies/{movie.movie_id}")

if __name__ == "__main__":
    connect_to_db(app)
    app.run(debug=True)
