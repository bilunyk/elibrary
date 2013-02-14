from elibrary import app as myapp, db, csrf
from unittest import TestCase
from elibrary.models import User, Book, Author
from flask import json


class ELibraryTest(TestCase):

    def setUp(self):
        myapp.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
        myapp.config['TESTING'] = True
        csrf._csrf_disable = True
        self.app = myapp.test_client()
        db.create_all()

    def tearDown(self):
        db.drop_all()

    def test_index(self):
        rv = self.app.get('/')
        self.assertEquals(rv.status_code, 200)

    def test_login(self):
        rv = self.app.get('/login/')
        self.assertEquals(rv.status_code, 200)
        User(name="admin", password="admin", email="admin@gmail.com").save()
        rv = self.app.post('/login/', data=dict(username="admin", password="admin"))
        # success if redirected
        self.assertEquals(rv.status_code, 302)
        rv = self.app.post('/login/', data=dict(username="admin11", password="admin"))
        # bad username/password
        self.assertEquals(rv.status_code, 200)
        self.assertIn("Incorrect username or password", rv.data)
        # no post data
        rv = self.app.post('/login/')
        self.assertIn("This field is required", rv.data)

    def test_register(self):
        rv = self.app.get('/register/')
        self.assertEquals(rv.status_code, 200)
        rv = self.app.post('/register/', data=dict(username="admin",
                                                   password="admin",
                                                   confirm="admin",
                                                   email="admin@gmail.com"))
        # success if redirected
        self.assertEquals(rv.status_code, 302)
        rv = self.app.post('/register/', data=dict(username="admin",
                                                   password="admin",
                                                   confirm="admin11",
                                                   email="admin@gmail.com"))
        self.assertEquals(rv.status_code, 200)
        self.assertIn('Passwords must match', rv.data)
        rv = self.app.post('/register/', data=dict(username="admin",
                                                   password="admin",
                                                   confirm="admin",
                                                   email="gmail.com"))
        self.assertEquals(rv.status_code, 200)
        self.assertIn('Invalid email address', rv.data)
        rv = self.app.post('/register/')
        self.assertEquals(rv.status_code, 200)
        self.assertIn('This field is required', rv.data)

    def test_search(self):
        rv = self.app.post('/')
        self.assertEquals(rv.status_code, 200)
        rv = self.app.post('/', data=dict(search_by="author",search_text="something"))
        self.assertEquals(json.loads(rv.data).get('result'), [])
        Book.create(title="Some funny book", info="Really funny book")
        rv = self.app.post('/', data=dict(search_by="name",search_text="some"))
        self.assertEquals(json.loads(rv.data).get('result')[0].get('title'), 'Some funny book')

    def test_books(self):
        # Need auth
        rv = self.app.get('/books/')
        self.assertEquals(rv.status_code, 401)
        # Method not allowed
        rv = self.app.post('/books/')
        self.assertEquals(rv.status_code, 405)
        User(name="admin", password="admin", email="admin@gmail.com").save()
        # Authenticate
        rv = self.app.post('/login/', data=dict(username="admin", password="admin"))
        rv = self.app.get('/books/')
        self.assertEquals(rv.status_code, 200)
        # Add new book
        a = Author.create(name="John Smith", info="Some info")
        rv = self.app.post('/book/', data=dict(title="Some book", info="Some book info", authors=[a]))
        self.assertEquals(rv.status_code, 302)
        rv = self.app.post('/book/')
        self.assertEquals(rv.status_code, 200)
        # invalid(empty) data
        self.assertIn("This field is required", rv.data)
        # Update book
        rv = self.app.get('/book/1/')
        self.assertEquals(rv.status_code, 200)
        rv = self.app.get('/book/2/')
        self.assertEquals(rv.status_code, 404)
        rv = self.app.post('/book/1/', data=dict(title="New title", info="Some book info"))
        self.assertEquals(rv.status_code, 302)
        rv = self.app.post('/book/1/', data=dict(info="Some book info"))
        self.assertEquals(rv.status_code, 200)
        self.assertIn("This field is required", rv.data)
        # Delete book
        rv = self.app.get('/book/1/delete/')
        self.assertEquals(rv.status_code, 302)
        rv = self.app.get('/book/1/delete/')
        self.assertEquals(rv.status_code, 404)

    def test_authors(self):
        # Need auth
        rv = self.app.get('/authors/')
        self.assertEquals(rv.status_code, 401)
        # Method not allowed
        rv = self.app.post('/authors/')
        self.assertEquals(rv.status_code, 405)
        User(name="admin", password="admin", email="admin@gmail.com").save()
        # Authenticate
        rv = self.app.post('/login/', data=dict(username="admin", password="admin"))
        rv = self.app.get('/authors/')
        self.assertEquals(rv.status_code, 200)
        # Add new author
        b = Book.create(title="Some book", info="Some book info")
        rv = self.app.post('/author/', data=dict(name="John Smith", info="Some info", books=[b]))
        self.assertEquals(rv.status_code, 302)
        rv = self.app.post('/author/')
        self.assertEquals(rv.status_code, 200)
        # invalid(empty) data
        self.assertIn("This field is required", rv.data)
        # Update author
        rv = self.app.get('/author/1/')
        self.assertEquals(rv.status_code, 200)
        rv = self.app.get('/author/2/')
        self.assertEquals(rv.status_code, 404)
        rv = self.app.post('/author/1/', data=dict(name="Eric Johnson", info="Some real info"))
        self.assertEquals(rv.status_code, 302)
        rv = self.app.post('/author/1/', data=dict(info="Some real info"))
        self.assertEquals(rv.status_code, 200)
        self.assertIn("This field is required", rv.data)
        # Delete author
        rv = self.app.get('/author/1/delete/')
        self.assertEquals(rv.status_code, 302)
        rv = self.app.get('/author/1/delete/')
        self.assertEquals(rv.status_code, 404)
