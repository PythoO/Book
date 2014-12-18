import os
from flask import Flask, render_template, request, url_for, redirect, jsonify, flash
from flask.ext.sqlalchemy import SQLAlchemy
import requests
import urllib2
import simplejson as json
from flask.ext.login import LoginManager, login_required, login_user, logout_user
from models import db, Book, User
from google_api import GoogleApi


app = Flask(__name__)
db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)

app.debug = os.environ['DEBUG']
app.secret_key = os.environ['SECRET_KEY']
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']

with app.app_context():
    db.create_all()


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')

    username = request.form['username']
    password = request.form['password']
    registered_user = User.query.filter_by(username=username, password=password).first()
    if registered_user is None:
        flash('Username or Password is invalid', 'error')
        return redirect(url_for('login'))
    login_user(registered_user)
    flash('Logged in successfully')
    return redirect(url_for('home'))


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/')
def home():
    all_books = Book.query.order_by(Book.title)
    return render_template("home.html", all_books=all_books)


@app.route('/insert', methods=['GET', 'POST'])
@login_required
def insert():
    if request.method == 'POST':
        isbn = request.form['isbn']

        googleApi = GoogleApi(isbn)
        googleApi.get_data()

        book = Book(isbn)
        book.title = googleApi.title
        book.authors = googleApi.authors
        book.authors = googleApi.authors
        db.session.add(book)
        db.session.commit()

        return redirect(url_for('home'))

    return render_template("insert.html")


@app.route('/modify', methods=['POST'])
def modify():
    book_id = int(request.form['book_id'])
    book = Book.query.filter_by(id=book_id).first()

    return render_template('modify.html', book=book)


@app.route('/update', methods=['POST'])
def update():
    if request.method == 'POST':
        book_id = request.form['book_id']
        isbn = request.form['isbn']
        title = request.form['title']
        authors = request.form['authors']

        book = Book.query.filter_by(id=book_id).first()
        book.isbn = isbn
        book.title = title
        book.authors = authors

        db.session.commit()

        return redirect(url_for('home'))


@app.route('/delete', methods=['POST'])
def delete():
    book_id = int(request.form['book_id'])
    book = Book.query.filter_by(id=book_id).first()
    db.session.delete(book)
    db.session.commit()
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run()