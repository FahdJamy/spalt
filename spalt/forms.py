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

	# functions validating the username and email
	def user_validator (self, username):
		user = User.query.filter_by(username=username.data).first()
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

