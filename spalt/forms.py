from flask import request, flash, redirect, url_for, session
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from spalt.models import User
from spalt import mysql, login_manager, bcrypt
from flask_login import UserMixin, login_user

class SignupForm(FlaskForm):
	# user login form fields
	fullname = StringField('Full Name', validators=[DataRequired(), Length(min=2, max=15)])
	username = StringField('Username', validators=[DataRequired(), Length(min=3, max=20)])
	email = StringField('Email', validators=[DataRequired(), Email()])
	password = PasswordField('Password', validators=[DataRequired()])
	password_confirm = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
	submit = SubmitField('SignUp')

	# username = request.form['username']
	# email = request.form['email']

	def user_validator (self, username):
		cur = mysql.connection.cursor()
		result = cur.execute("SELECT * FROM userinfo where email = %s" [email])
		undata = cur.fetchone()
		usernamedt = undata['username']
		if usernamedt == username.data :
			raise ValidationError ('Username is already taken, please choose another different Username')
		cur.close()

	def user_validator (self, email):
		cur = mysql.connection.cursor()
		result = cur.execute("SELECT * FROM userinfo where email = %s" [email])
		undata = cur.fetchone()
		emaildt = undata['email']
		if emaildt == email.data :
			raise ValidationError ('Username is already taken, please choose another different Username')
		cur.close()


	# functions validating the username and email
	def user_validator (self, username):
		user = User.query.filterby(username=username.data).first()
		if user:
			raise ValidationError ('Username is already taken, please choose another different Username')


	def email_validator(self,email):
		email = User.query.filter_by(email=email.data).first()
		if email:
			raise ValidationError ('Sorry email already exists, please sign in using another email')
		
class LoginForm(FlaskForm):
	email = StringField('Email', validators=[DataRequired(), Email()])
	password = PasswordField('Password', validators=[DataRequired()])
	remember = BooleanField('Remember me')
	submit = SubmitField('Login')
	# user login form fields

class PostForm(FlaskForm):
	title = StringField('Title', validators=[DataRequired()])
	content = TextAreaField('Content', validators=[DataRequired()])
	forum = StringField('Type', validators=[DataRequired()])
	submit = SubmitField('main')

class AccountForm(FlaskForm):
	fullname = StringField('Full Name', validators=[DataRequired(), Length(min=2, max=15)])
	username = StringField('Username', validators=[DataRequired(), Length(min=3, max=20)])
	email = StringField('Email', validators=[DataRequired(), Email()])
	image_file = FileField('Update Profile Picture', validators=[DataRequired(['mpg', 'jpg', 'png'])])
	submit = SubmitField('Update')


@login_manager.user_loader
def user_load(user_id):
	cur = mysql.connection.cursor()
	dbres = cur.execute("SELECT * FROM userinfo WHERE username = %s", [username])

	# def is_authenticated(self):
	# 	return True
	# def is_active(self):
	# 	return True
	# def is_anonymous(self):
	# 	return True
	# def get_id(self):
	# 	return unicode(self.id)
	# get_id()

	return cur.fetchone(dbres.id == int(user_id))
	cur.close()


class MysqlResults(UserMixin):

	
	# def is_active(self, id):
	# 	user_id = user_loader()
	# 	if self.id == user_id:
	# 		return True
	# 	return ("sorry we could'nt log you in")


	def password_returner(email):
		cur = mysql.connection.cursor()
		email_res = cur.execute("SELECT * FROM userinfo where email = %s", [email])

		if email_res > 0:
			user_email = cur.fetchone()
			real_email = user_email['email']
			dbpass = user_email['password']
			return str(dbpass)

		flash('Login unsuccessful, check email and password please', 'danger')
		return redirect(url_for('login'))
		cur.close()

	def email_returner(email):
		cur = mysql.connection.cursor()
		email_res = cur.execute("SELECT * FROM userinfo where email = %s", [email])
		if email_res == 0:
			# flash('sorry thats an invalid email, please login in with a valid email')
			return redirect('login')
		data_user = cur.fetchone()
		user_email = data_user['email']
		return str(user_email)
		cur.close()


	def user_returner(email):
			cur = mysql.connection.cursor()
			email_res = cur.execute("SELECT * FROM userinfo where email = %s", [email])

			if email_res > 0:
				user_email = cur.fetchone()
				dbuser = user_email['username']
				return str(dbuser)

			flash('Login unsuccessful, check email and password please', 'danger')
			return redirect(url_for('login'))
			cur.close()
