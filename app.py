from flask import Flask, render_template, request, redirect, url_for, flash
from Database_Entitys import db
from DataManager import DataManager
from dotenv import load_dotenv
import secrets

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_hex(16)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///movie.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()

data_manager = DataManager()


@app.route('/')
def home():
    users = data_manager.get_users()
    return render_template('home.html', users=users)


@app.route('/users', methods=['POST'])
def add_user():
    username = request.form.get('username', '').strip()
    if username:
        data_manager.add_user(username)
        flash(f'User "{username}" successfully added!', 'success')
    else:
        flash('Username is required!', 'error')
    return redirect(url_for('home'))


@app.route('/users/<int:user_id>/movies', methods=['GET'])
def user_movies(user_id):
    movies = data_manager.get_movies(user_id)
    return render_template('user_movies.html', user_id=user_id, movies=movies)


@app.route('/users/<int:user_id>/movies', methods=['POST'])
def add_movie(user_id):
    title = request.form.get('title')
    if title:
        movie = data_manager.add_movie(user_id, title)
        if movie:
            flash(f'Movie "{movie.title}" successfully added!', 'success')
        else:
            flash(f'Could not find movie "{title}" in OMDB database. Please check the title or API key.', 'error')
    else:
        flash('Movie title is required!', 'error')
    return redirect(url_for('user_movies', user_id=user_id))


@app.route('/users/<int:user_id>/movies/<int:movie_id>/update', methods=['POST'])
def update_movie(user_id, movie_id):
    new_title = request.form.get('new_title')
    if new_title:
        movie = data_manager.update_movie(movie_id, new_title)
        if movie:
            flash(f'Movie title updated to "{new_title}"!', 'success')
        else:
            flash('Movie not found!', 'error')
    else:
        flash('New title is required!', 'error')
    return redirect(url_for('user_movies', user_id=user_id))


@app.route('/users/<int:user_id>/movies/<int:movie_id>/delete', methods=['POST'])
def delete_movie(user_id, movie_id):
    success = data_manager.delete_movie(movie_id)
    if success:
        flash('Movie successfully deleted!', 'success')
    else:
        flash('Movie not found!', 'error')
    return redirect(url_for('user_movies', user_id=user_id))


if __name__ == '__main__':
    app.run(debug=True)