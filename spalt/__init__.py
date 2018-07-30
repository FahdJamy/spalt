from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mysqldb import MySQL
from flask_login import UserMixin
from flask_bcrypt import Bcrypt
from flask_mail import Mail
from spalt.config import Config

db = SQLAlchemy()

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

# # db condig for MySQL
# app.config['MYSQL_HOST'] = 'localhost'
# app.config['MYSQL_USER'] = 'root'
# app.config['MYSQL_DB'] = 'spalt'
# app.config['MYSQL_PASSWORD'] = ''
# app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mail = Mail()

# mysql = MySQL()
bcrypt = Bcrypt()


def appCreator(config_name=Config):
	app = Flask(__name__)
	app.config.from_object(Config)

	db.init_app(app)
	login_manager.init_app(app)
	mail.init_app(app)
	bcrypt.init_app(app)

	from spalt.users.routes import users
	from spalt.blogs.routes import blogs
	from spalt.home.routes import home
	app.register_blueprint(users)
	app.register_blueprint(blogs)
	app.register_blueprint(home)

	return app

