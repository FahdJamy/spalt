from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField
from wtforms import StringField, SubmitField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Email, ValidationError, EqualTo, Length
from spalt.models import User


class SignupForm(FlaskForm):
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


class AccountForm(FlaskForm):
	fullname = StringField('Full Name', validators=[Length(min=2, max=15)])
	email = StringField('Email', validators=[Email()])
	image_file = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png', 'mpg'])])
	submit = SubmitField('Update')

	def validate_fullname(self, fullname):
		if fullname.data != current_user.fullname:
			user = User.query.filter_by(fullname=fullname.data).first()
			if user:
				raise ValidationError ('Username is already taken, please choose another different Username')

	def validate_email(self, email):
		if email.data != current_user.email:
				user = User.query.filter_by(email=email.data).first()
				if user:
					raise ValidationError ('Sorry Email is already taken, please choose another email address')

