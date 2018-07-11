from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo

class SignupForm(FlaskForm):
	# user login form fields
	firstName = StringField('First Name', validators=[DataRequired(), Length(min=2, max=15)])
	lastName = StringField('Last Name', validators=[DataRequired(), Length(min=2, max=15)])
	username = StringField('Username', validators=[DataRequired(), Length(min=3, max=20)])
	email = StringField('Email', validators=[DataRequired(), Email()])
	password = PasswordField('Password', validators=[DataRequired()])
	password_confirm = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
	submit = SubmitField('SignUp')

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

