import os
from flask import Flask, render_template, request, url_for, redirect, jsonify
from flask.ext.sqlalchemy import SQLAlchemy
import requests
import urllib2
import simplejson as json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/book.db'
#app.debug = True
db = SQLAlchemy(app)


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    authors = db.Column(db.String(200))
    isbn = db.Column(db.Integer)

    def __init__(self, isbn):
        self.isbn = isbn

    def __repr__(self):
        return '<TITLE %r>' % self.title


@app.route('/')
def home():
    all_books = Book.query.all()
    return render_template("home.html", all_books=all_books)


@app.route('/insert', methods=['GET', 'POST'])
def insert():
    if request.method == 'POST':
        isbn = request.form['isbn']
        google_url = 'https://www.googleapis.com/books/v1/volumes?q=%s+isbn' % isbn
        response = requests.get(google_url)
        html = response.text
        #print html.encode('utf-8')
        try:
            data = json.loads(html)
        except Exception as e:
            return e.message
        title = data['items'][0][u'volumeInfo'][u'title']
        string_authors = ''
        try:
            authors = data['items'][0][u'volumeInfo'][u'authors']
            for auth in authors:
                string_authors += auth + ', '
        except KeyError:
            pass
        book = Book(isbn)
        book.title = title
        book.authors = string_authors
        db.session.add(book)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template("insert.html")


@app.route('/delete', methods=['POST'])
def delete():
    book_id = int(request.form['book_id'])
    book = Book.query.filter_by(id=book_id).first()
    db.session.delete(book)
    db.session.commit()
    return redirect(url_for('home'))