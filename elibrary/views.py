from flask import render_template, redirect, flash, jsonify, request
from flask.views import MethodView, View
from flask.ext.login import login_user, logout_user, login_required
from elibrary import app
from models import Author, Book, User
from forms import (RegistrationForm, LoginForm, SearchForm, AuthorForm,
                   BookForm)


class LoginView(MethodView):

    def __init__(self, *args, **kwargs):
        super(LoginView, self).__init__(*args, **kwargs)
        self.form = LoginForm()

    def get(self):
        return render_template('login.html', form=self.form)

    def post(self):
        if self.form.validate_on_submit():
            user = User.query.filter_by(name=self.form.username.data).first()
            if user and user.check_password(self.form.password.data):
                login_user(user)
                return redirect('/')
            else:
                flash('Incorrect username or password')

        return render_template('login.html', form=self.form)


app.add_url_rule('/login/', view_func=LoginView.as_view('login'))


class RegistrationView(MethodView):

    def __init__(self, *args, **kwargs):
        super(RegistrationView, self).__init__(*args, **kwargs)
        self.form = RegistrationForm()

    def get(self):
        return render_template('register.html', form=self.form)

    def post(self):
        if self.form.validate_on_submit():
            user = User(name=self.form.username.data,
                        email=self.form.email.data,
                        password=self.form.password.data)
            user.save()
            login_user(user)
            return redirect('/')

        print self.form.errors
        return render_template('register.html', form=self.form)

app.add_url_rule('/register/', view_func=RegistrationView.as_view('register'))


@login_required
@app.route('/logout/')
def logout():
    logout_user()
    return redirect('/')


class SearchView(MethodView):

    def get(self):
        return render_template('index.html')

    def post(self):
        form = SearchForm()
        if form.validate_on_submit():
            search_by, search_text = form.search_by.data, form.search_text.data
            search_pattern = "%{0}%".format(search_text)
            if search_by == 'name':
                books = Book.query.filter(Book.title.like(search_pattern)).all()
            else:
                books = Book.query.join(Author.books).filter(Author.name.like(search_pattern)).all()
            return jsonify(result=[book.as_dict() for book in books])

        return render_template('index.html', form=form)

app.add_url_rule('/', view_func=SearchView.as_view('index'))


class BookCreateView(View):

    decorators = [login_required]
    methods = ['GET', 'POST']

    def dispatch_request(self):
        form = BookForm()
        form.authors.query = Author.query.all()
        if request.method == "POST":
            if form.validate_on_submit():
                obj = Book()
                form.populate_obj(obj)
                obj.save()
                return redirect("/books/")
        return render_template("book_add.html", form=form)

app.add_url_rule('/book/', view_func=BookCreateView.as_view('book_add'))


class AuthorCreateView(View):

    decorators = [login_required]
    methods = ['GET', 'POST']

    def dispatch_request(self):
        form = AuthorForm()
        form.books.query = Book.query.all()
        if request.method == "POST":
            if form.validate_on_submit():
                obj = Author()
                form.populate_obj(obj)
                obj.save()
                return redirect("/authors/")
        return render_template("author_add.html", form=form)

app.add_url_rule('/author/', view_func=AuthorCreateView.as_view('author_add'))


class BookEditView(View):

    decorators = [login_required]
    methods = ['GET', 'POST']

    def dispatch_request(self, obj_id):
        obj = Book.query.get_or_404(obj_id)
        form = BookForm(obj=obj)
        form.authors.query = Author.query.join(Book.authors).union(Author.query)
        if request.method == "POST":
            if form.validate_on_submit():
                form.populate_obj(obj)
                obj.save()
                return redirect("/books/")
        return render_template("book_edit.html", form=form, obj=obj)

app.add_url_rule('/book/<int:obj_id>/',
                 view_func=BookEditView.as_view('book_edit'))


class AuthorEditView(View):

    decorators = [login_required]
    methods = ['GET', 'POST']

    def dispatch_request(self, obj_id):
        obj = Author.query.get_or_404(obj_id)
        form = AuthorForm(obj=obj)
        form.books.query = Book.query.join(Author.books).union(Book.query)
        if request.method == "POST":
            if form.validate_on_submit():
                form.populate_obj(obj)
                obj.save()
                return redirect("/authors/")
        return render_template("author_edit.html", form=form, obj=obj)

app.add_url_rule('/author/<int:obj_id>/',
                 view_func=AuthorEditView.as_view('author_edit'))


class DeleteView(View):
    """
    Abstract view for data deletion
    """

    decorators = [login_required]
    methods = ['GET', 'POST']

    def get_model(self):
        raise NotImplementedError()

    def get_redirect_url(self):
        raise NotImplementedError()

    def dispatch_request(self, obj_id):
        model_cls = self.get_model()
        obj = model_cls.query.get_or_404(obj_id)
        obj.delete()
        return redirect(self.get_redirect_url())


class BookDeleteView(DeleteView):

    def get_model(self):
        return Book

    def get_redirect_url(self):
        return "/books/"

app.add_url_rule('/book/<int:obj_id>/delete/',
                 view_func=BookDeleteView.as_view('book_delete'))


class AuthorDeleteView(DeleteView):

    def get_model(self):
        return Author

    def get_redirect_url(self):
        return "/authors/"

app.add_url_rule('/author/<int:obj_id>/delete/',
                 view_func=AuthorDeleteView.as_view('author_delete'))


class ListView(View):
    """
    Abstract list view
    """

    decorators = [login_required]
    methods = ['GET']

    def get_model(self):
        raise NotImplementedError

    def get_template(self):
        raise NotImplementedError

    def dispatch_request(self):
        model = self.get_model()
        objects = model.query.all()
        return render_template(self.get_template(),
                               objects=[obj.as_dict() for obj in objects])


class BookListView(ListView):

    def get_template(self):
        return "book_list.html"

    def get_model(self):
        return Book

app.add_url_rule('/books/', view_func=BookListView.as_view('book_list'))


class AuthorListView(ListView):

    def get_template(self):
        return "author_list.html"

    def get_model(self):
        return Author

app.add_url_rule('/authors/', view_func=AuthorListView.as_view('author_list'))
