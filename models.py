"""Models for Blogly."""
import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


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

    created_at = db.Column(db.DateTime, nullable=False,
                           default=datetime.datetime.utcnow)

    user_id = db.Column(db.Integer, db.ForeignKey(
        "users.id", ondelete="CASCADE"), nullable=False)

    @property
    def readable_date(self):
        """Returns a user readable date"""

        return self.created_at.strftime("%a %b %d %Y, %I:%M %p")


class PostTag(db.Model):
    """post tags"""

    __tablename__ = 'posts_tags'

    post_id = db.Column(db.Integer, db.ForeignKey(
        'posts.id', ondelete='CASCADE'), primary_key=True)

    tag_id = db.Column(db.Integer, db.ForeignKey(
        'tags.id', ondelete='CASCADE'), primary_key=True)


class Tag(db.Model):
    """Tags"""

    __tablename__ = 'tags'

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(15), unique=True, nullable=False)

    posts = db.relationship(
        'Post',
        secondary="posts_tags",
        cascade="all,delete-orphan",
        backref="tags",
    )


def connect_db(app):
    db.app = app
    db.init_app(app)
