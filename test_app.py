from unittest import TestCase
from app import app
from models import User, Post, db

app.config['TESTING'] = True
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_ECHO'] = False

db.drop_all()


class BloglyTest (TestCase):

    def setUp(self):
        db.create_all()
        user1 = User(first_name='John', last_name='Doe', image_url='None')
        print(f'first call = {user1.id}')
        print(f'second call = {user1.first_name}')
        db.session.add(user1)
        db.session.commit()
        print(f'third call = {user1.id}')
        p1 = Post(title='First Post',
                  content='Starting comment', user_id='1')

        p2 = Post(title='Second Post', content='Next', user_id='1')

        db.session.add(p1)
        db.session.add(p2)
        db.session.commit()
        print(f'last call = {user1.id}')
        self.user_id = user1.id

    def tearDown(self):
        db.drop_all()

    def test_users(self):
        with app.test_client() as client:

            resp = client.get('/users')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('John Doe', html)

    def test_delete(self):
        with app.test_client() as client:

            resp = client.post(
                f'/user/{self.user_id}/delete', follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertNotIn('John Doe', html)

    def test_detail(self):
        with app.test_client() as client:

            resp = client.get(f"/users/{self.user_id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('John Doe', html)

    def test_new_user(self):
        with app.test_client() as client:
            TEST_IMG_ROUTE = 'https://images.unsplash.com/photo-1511367461989-f85a21fda167?ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&ixlib=rb-1.2.1&auto=format&fit=crop&w=889&q=80'

            d = {"first_name": "Test", "last_name": "Case",
                 "image_url": TEST_IMG_ROUTE}
            resp = client.post('/users/new', data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Test Case', html)
