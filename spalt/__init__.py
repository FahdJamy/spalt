from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mysqldb import MySQL
from flask_login import UserMixin
from flask_bcrypt import Bcrypt
from flask_mail import Mail

app = Flask(__name__)
# applictions secret key
app.config['SECRET_KEY'] = '3da8dfc5ed7003c124b7294ab73d31dda0b11c6b'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///spaltdb.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/spalt'
db = SQLAlchemy(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

# db condig for MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_DB'] = 'spalt'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mail = Mail(app)

mysql = MySQL(app)
bcrypt = Bcrypt(app)

from spalt.users.routes import users
from spalt.blogs.routes import blogs
from spalt.home.routes import home
app.register_blueprint(users)
app.register_blueprint(blogs)
app.register_blueprint(home)