from datetime import datetime

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
            'apikey': str(self.omdb_api_key).strip(),
            't': str(title).strip()
        }
        response = requests.get(self.omdb_url, params=params)
        data = response.json()

        if data.get('Response') == 'True':
            # Parse publication date from OMDB
            # OMDB returns 'Released' as 'DD MMM YYYY' (e.g., '14 Oct 1994')
            # or 'Year' as string (e.g., '1994', '2019-2021')
            publication_date = None
            try:
                # Try to parse the 'Released' field first (more precise)
                released = data.get('Released', '')
                if released and released != 'N/A':
                    publication_date = datetime.strptime(released, '%d %b %Y')
                else:
                    # Fall back to 'Year' field - extract first 4 digits
                    year_str = data.get('Year', '')
                    if year_str and year_str != 'N/A':
                        # Extract first year from strings like '2019-2021' or '1994'
                        year = int(year_str[:4])
                        publication_date = datetime(year, 1, 1)
            except (ValueError, IndexError):
                # If parsing fails, set to None
                publication_date = None

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