import sqlalchemy
from sqlalchemy import orm, Column, Integer, String, ForeignKey, DateTime
engine = sqlalchemy.create_engine("sqlite:///movie.db")
base = orm.declarative_base()

class User(base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(80), unique=True)

    movies = orm.relationship('Movie', backref='user', lazy=True)

    def __repr__(self):
        return f'<User {self.username}>'

class Movie(base):
    __tablename__ = 'movies'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    title = Column(String(120), unique=True)
    publication_date = Column(DateTime)
    director = Column(String(80))
    img_url = Column(String(200))

    def __repr__(self):
        return f'<Movie {self.title}>'