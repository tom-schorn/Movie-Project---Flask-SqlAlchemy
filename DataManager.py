from Database_Entitys import db, User, Movie
import requests
import os


class DataManager():
    def __init__(self):
        self.omdb_api_key = os.getenv('OMDB_API_KEY')
        self.omdb_url = 'http://www.omdbapi.com/'

    def add_user(self, username):
        user = User(username=username)
        db.session.add(user)
        db.session.commit()
        return user

    def get_users(self):
        return User.query.all()

    def add_movie(self, user_id, title):
        # Fetch movie data from OMDB API
        params = {
            'apikey': self.omdb_api_key,
            't': title
        }
        response = requests.get(self.omdb_url, params=params)
        data = response.json()

        if data.get('Response') == 'True':
            publication_date = data.get('Year', '')
            director = data.get('Director', '')
            img_url = data.get('Poster', '')

            movie = Movie(
                user_id=user_id,
                title=data.get('Title', title),
                publication_date=publication_date,
                director=director,
                img_url=img_url
            )
            db.session.add(movie)
            db.session.commit()
            return movie
        return None

    def get_movies(self, user_id):
        return Movie.query.filter_by(user_id=user_id).all()

    def update_movie(self, movie_id, new_title):
        movie = Movie.query.get(movie_id)
        if movie:
            movie.title = new_title
            db.session.commit()
            return movie
        return None

    def delete_movie(self, movie_id):
        movie = Movie.query.get(movie_id)
        if movie:
            db.session.delete(movie)
            db.session.commit()
            return True
        return False