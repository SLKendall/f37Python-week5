"""This module is responsible for CRUD operations in our Postgresql dtabse."""

from model import db, connect_to_db, User, Movie, Rating

def create_user(email, password):
    new_user = User(email=email, password=password)
    return new_user

def get_users():
    return User.query.all()

def get_user_by_id(user_id):
    return User.query.get(user_id)

def get_user_by_email(email):
    return User.query.filter_by(email=email).first()

def create_movie(title, overview, release_date, poster_path):
    new_movie = Movie(
        title=title,
        overview=overview,
        release_date=release_date,
        poster_path=poster_path
    )
    return new_movie

def get_movies():
    return Movie.query.all()

def get_movie_by_id(movie_id):
    return Movie.query.get(movie_id)

def create_rating(user, movie, score):
    new_rating=Rating(
        user=user,
        movie=movie,
        score=score
    )
    return new_rating

if __name__ == "__main__":
    from server import app
    connect_to_db(app)