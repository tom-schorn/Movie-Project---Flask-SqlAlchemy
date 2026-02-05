from Database_Entitys import db, User, Movie


class DataManager():
    def __init__(self):
        pass

    def add_user(self, username):
        user = User(username=username)
        db.session.add(user)
        db.session.commit()
        return user

    def get_users(self):
        return User.query.all()

    def add_movie(self, user_id, title, publication_date, director, img_url):
        movie = Movie(
            user_id=user_id,
            title=title,
            publication_date=publication_date,
            director=director,
            img_url=img_url
        )
        db.session.add(movie)
        db.session.commit()
        return movie

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