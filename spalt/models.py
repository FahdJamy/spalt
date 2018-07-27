from spalt import login_manager, db
from flask_login import UserMixin
from datetime import datetime
from flask import current_app

# handles sessions
@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))

# UserMixin help in session handlin' including. is user active, user annonymous, is user authenticated
class User(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key=True)
	fullname = db.Column(db.String(50), nullable=False)
	username = db.Column(db.String(30), nullable=False, unique=True)
	email = db.Column(db.String(120), nullable=False, unique=True)
	password = db.Column(db.String(60), nullable=False)
	imagefile = db.Column(db.String(20), nullable=False, default='default.jpg')
	blogs = db.relationship('Blogs', backref='author', lazy=True)

	# what the db returns
	def __repr__(self):
		return f"User('{self.fullname}', '{self.username}', '{self.email}', '{self.password}')"

class Blogs(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	topic = db.Column(db.String(100), nullable=False)
	content = db.Column(db.Text, nullable=False)
	forum_type = db.Column(db.String(100), nullable=False, default='Entertainment')
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
	date_created = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

	# what the db returns
	def __repr__(self):
		return f"User('{self.topic}', '{self.content}', '{self.forum_type}')"
