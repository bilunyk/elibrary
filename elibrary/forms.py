from flask.ext.wtf import (Form, TextField, TextAreaField, PasswordField,
                           RadioField, QuerySelectMultipleField, Required,
                           EqualTo, Email)
from models import Author, Book


class LoginForm(Form):
    username = TextField(u'Username', validators=[Required()])
    password = PasswordField(u'Password', validators=[Required()])


class RegistrationForm(Form):
    username = TextField(u'Username', validators=[Required()])
    email = TextField(u'Email', validators=[Required(), Email()])
    password = PasswordField(u'Password', validators=[Required(), EqualTo('confirm', message='Passwords must match')])
    confirm = PasswordField(u'Confirm password', validators=[Required()])


class SearchForm(Form):
    search_text = TextField(u'SearchText', validators=[Required()])
    search_by = RadioField(u'SearchBy',
                           choices=[('name', 'Name'), ('author', 'Author')],
                           validators=[Required()])


class BookForm(Form):
    title = TextField(u'Title', validators=[Required()])
    info = TextAreaField(u'Book Info', validators=[Required()])
    authors = QuerySelectMultipleField(u'Select authors')


class AuthorForm(Form):
    name = TextField(u'Name', validators=[Required()])
    info = TextAreaField(u'Author Info', validators=[Required()])
    books = QuerySelectMultipleField(u'Select books')
