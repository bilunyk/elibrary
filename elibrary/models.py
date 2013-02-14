from elibrary import db, login_manager
from flask.ext.login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


books_authors = db.Table('books_authors',
                         db.Column('book_id', db.Integer, db.ForeignKey('books.id')),
                         db.Column('author_id', db.Integer, db.ForeignKey('authors.id'))
                         )


class CRUDMixin(object):

    @classmethod
    def create(cls, commit=True, **kwargs):
        obj = cls(**kwargs)
        db.session.add(obj)
        if commit:
            db.session.commit()
        return obj

    @classmethod
    def get(cls, id):
        return cls.query.get(id)

    def update(self, commit=True, **kwargs):
        for k, v in kwargs.iteritems():
            setattr(self, k, v)
        if commit:
            db.session.commit()
        else:
            return self

    def save(self, commit=True):
        db.session.add(self)
        if commit:
            db.session.commit()
        else:
            return self

    def delete(self, commit=True):
        db.session.delete(self)
        if commit:
            db.session.commit()


class User(db.Model, CRUDMixin, UserMixin):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40))
    password = db.Column(db.String(40))
    email = db.Column(db.String(40), unique=True)

    def __init__(self, name, password, email):
        self.name = name
        self.password = generate_password_hash(password)
        self.email = email

    def check_password(self, password):
        return check_password_hash(self.password, password)


class Book(db.Model, CRUDMixin):

    __tablename__ = "books"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), unique=True)
    info = db.Column(db.String(512))

    def __repr__(self):
        return "{0}".format(self.title)

    def as_dict(self):
        return {"id": self.id, "title": self.title, "info": self.info,
                "authors": [a.name for a in self.authors.all()]}


class Author(db.Model, CRUDMixin):

    __tablename__ = "authors"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), unique=True)
    info = db.Column(db.String(512))
    books = db.relationship('Book', secondary=books_authors,
                            backref=db.backref('authors', lazy='dynamic'))

    def __repr__(self):
        return "{0}".format(self.name)

    def as_dict(self):
        return {"id": self.id, "name": self.name, "info": self.info,
                "books": [b.title for b in self.books]}


# User loader
@login_manager.user_loader
def load_user(id):
    return User.query.get(id)
