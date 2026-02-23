from datetime import datetime

from Database_Entitys import db, User, Movie
from sqlalchemy.exc import IntegrityError
import requests
import os


class DataManager():
    """Manages database operations for users and movies."""

    def __init__(self):
        """Initialize DataManager with OMDB API configuration."""
        self.omdb_api_key = os.getenv('OMDB_API_KEY')
        self.omdb_url = 'http://www.omdbapi.com/'

    def add_user(self, username):
        """Add a new user to the database.

        Args:
            username: The username string.

        Returns:
            The created User object.
        """
        user = User(username=username)
        db.session.add(user)
        db.session.commit()
        return user

    def get_users(self):
        """Retrieve all users from the database.

        Returns:
            List of User objects.
        """
        return User.query.all()

    def add_movie(self, user_id, title):
        """Fetch movie data from OMDB and add it to the user's list.

        Args:
            user_id: The ID of the user.
            title: The movie title to search for.

        Returns:
            The created Movie object, or None if not found in OMDB.

        Raises:
            ValueError: If the movie already exists in the user's list.
        """
        params = {
            'apikey': str(self.omdb_api_key).strip(),
            't': str(title).strip()
        }
        response = requests.get(self.omdb_url, params=params)
        data = response.json()

        if data.get('Response') == 'True':
            publication_date = None
            try:
                released = data.get('Released', '')
                if released and released != 'N/A':
                    publication_date = datetime.strptime(released, '%d %b %Y')
                else:
                    year_str = data.get('Year', '')
                    if year_str and year_str != 'N/A':
                        year = int(year_str[:4])
                        publication_date = datetime(year, 1, 1)
            except (ValueError, IndexError):
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
            try:
                db.session.commit()
            except IntegrityError:
                db.session.rollback()
                raise ValueError(f'"{data.get("Title", title)}" is already in your list.')
            return movie
        return None

    def get_movies(self, user_id):
        """Retrieve all movies for a specific user.

        Args:
            user_id: The ID of the user.

        Returns:
            List of Movie objects belonging to the user.
        """
        return Movie.query.filter_by(user_id=user_id).all()

    def update_movie(self, movie_id, new_title):
        """Update the title of an existing movie.

        Args:
            movie_id: The ID of the movie to update.
            new_title: The new title string.

        Returns:
            The updated Movie object, or None if not found.

        Raises:
            ValueError: If the new title already exists in the user's list.
        """
        movie = Movie.query.get(movie_id)
        if movie:
            movie.title = new_title
            try:
                db.session.commit()
            except IntegrityError:
                db.session.rollback()
                raise ValueError(f'"{new_title}" is already in your list.')
            return movie
        return None

    def delete_movie(self, movie_id):
        """Delete a movie from the database.

        Args:
            movie_id: The ID of the movie to delete.

        Returns:
            True if deleted successfully, False if not found.
        """
        movie = Movie.query.get(movie_id)
        if movie:
            db.session.delete(movie)
            db.session.commit()
            return True
        return False
