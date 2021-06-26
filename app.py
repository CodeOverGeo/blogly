"""Blogly application."""

from flask import Flask, request, render_template
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

app.config['SECRET_KEY'] = "Hamilton"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app)
db.create_all()

@app.route('/get')
def get():
    pass

@app.route('/users')
def user():
    return render_template ('users.html')

@app.route('/new_user')
def new_user():
    pass

@app.route('/user_detail')
def user_detail():
    return render_template ('user_detail.html')

@app.route('/edit_user')
def edit_user():
    pass
