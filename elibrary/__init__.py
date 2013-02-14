from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

from flask.ext.login import LoginManager
from flask.ext.seasurf import SeaSurf

app = Flask(__name__)
app.config['SECRET_KEY'] = "Smthreallysecret"
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.db'
# disable wtforms csrf because seasurf are using
app.config['CSRF_ENABLED'] = False
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
csrf = SeaSurf(app)

import elibrary.views
