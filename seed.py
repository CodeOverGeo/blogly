from app import db
from models import User, Post, db, Tag, PostTag

db.drop_all()
db.create_all()

user1 = User(first_name='James', last_name='Riddick')
user2 = User(first_name='Kimberly', last_name='Blaire')

p1 = Post(title='First Post',
          content='Obligatory wrote this on mobile. This is my first post.', user_id='1')
p3 = Post(title='Second Post',
          content='Obligatory wrote this on mobile. This is my second post.', user_id='1')
p2 = Post(title='What''s going on?',
          content='Can''t wait to interact with everyone on here', user_id='2')
p4 = Post(title='What''s going on, now?',
          content='Can''t wait to interact with everyone on here again', user_id='2')

db.session.add(user1)
db.session.add(user2)

db.session.commit()

db.session.add(p1)
db.session.add(p2)
db.session.add(p3)
db.session.add(p4)

db.session.commit()
