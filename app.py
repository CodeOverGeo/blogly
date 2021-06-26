"""Blogly application."""

from flask import Flask, request, render_template, redirect
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User

app = Flask(__name__, static_url_path='/static')
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

app.config['SECRET_KEY'] = "Hamilton"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
toolbar = DebugToolbarExtension(app)

connect_db(app)
db.create_all()

@app.route('/')
def root():
    """Root route redirects to user list"""
    return redirect ('/users')

@app.route('/get')
def get():
    pass

@app.route('/users')
def users():
    users = User.query.order_by(User.last_name, User.first_name).all()
    return render_template ('users/users.html', users=users)

@app.route('/users/new')
def new_user_page():
    """Show a form to create a new user"""

    return render_template('users/new.html')

@app.route('/users/new', methods=['POST'])
def create_user():
    """Get form values from new user page and create a new user"""

    new_user = User(
        first_name=request.form['first_name'],
        last_name=request.form['last_name'],
        image_url=request.form.get('image_url') or None
    )

    db.session.add(new_user)
    db.session.commit()

    return redirect("/users")

@app.route('/user/<int:user_id>')
def user_show(user_id):
    """Show detail page for specific user"""

    user = User.query.get_or_404(user_id)
    return render_template('users/detail.html', user = user)


@app.route('/users/<int:user_id>')
def user_detail(user_id):

    user = User.query.get_or_404(user_id)
    return render_template ('users/detail.html', user = user)

@app.route('/users/<int:user_id>/edit')
def edit_user(user_id):
    """Show a form to edit a specific user"""

    user = User.query.get_or_404(user_id)
    return render_template('users/edit.html', user = user)

@app.route('/users/<int:user_id>/edit', methods = ['POST'])
def update_user(user_id):
    """Get edit user form values and update database"""

    user = User.query.get_or_404(user_id)
    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    user.image_url = request.form.get('image_url') or None

    db.session.add(user)
    db.session.commit()

    return redirect('/users')

@app.route('/user/<int:user_id>/delete', methods=['POST'])
def user_delete(user_id):
    """Deletes user based off of delete request"""

    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()

    return redirect('/users')




    
