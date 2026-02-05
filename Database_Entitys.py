from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import orm, Column, Integer, String, ForeignKey, DateTime

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(80), unique=True)

    movies = orm.relationship('Movie', backref='user', lazy=True)

    def __repr__(self):
        return f'<User {self.username}>'

class Movie(db.Model,):
    __tablename__ = 'movies'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    title = Column(String(120), unique=True)
    publication_date = Column(DateTime)
    director = Column(String(80))
    img_url = Column(String(200))

    def __repr__(self):
        return f'<Movie {self.title}>'