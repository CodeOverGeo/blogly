"""Models for Blogly."""
import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def connect_db(app):
    db.app = app
    db.init_app(app)


DEFAULT_IMAGE_URL = "/static/generic_profile.png"


class User(db.Model):
    """User"""

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)

    first_name = db.Column(db.String(30),
                           nullable=False)

    last_name = db.Column(db.String(30),
                          nullable=False)

    image_url = db.Column(db.String, nullable=False, default=DEFAULT_IMAGE_URL)

    posts = db.relationship("Post", backref="user",
                            cascade="all, delete-orphan")

    @property
    def full_name(self):
        """Return full name of user."""

        return f"{self.first_name} {self.last_name}"


class Post(db.Model):
    """Posts"""

    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(30), nullable=False)

    content = db.Column(db.String(100), nullable=False)

    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    user_id = db.Column(db.Integer, db.ForeignKey(
        "users.id"), nullable=False)

    # users = db.relationship('User', backref='posts',
    #                         cascade='all, delete-orphan')

    @property
    def readable_date(self):
        """Returns a user readable date"""

        return self.created_at.strftime("%a %b %d %Y, %I:%M %p")
