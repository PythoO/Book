import os
from flask import Flask, render_template, request, url_for, redirect
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
db = SQLAlchemy(app)


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    isbn = db.Column(db.Integer)

    def __init__(self, isbn):
        self.isbn = isbn

    def __repr__(self):
        return '<TITLE %r>' % self.title


@app.route('/')
def home():
    all_books = Book.query.all()
    return render_template("home.html", all_books = all_books)


@app.route('/insert', methods=['GET', 'POST'])
def insert():
    if request.method == 'POST':
        isbn = int(request.form['isbn'])
        return redirect(url_for('home'))
    return render_template("insert.html")


@app.route('/delete/{id}')
def delete():
    return render_template("insert.html")