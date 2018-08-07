from flask import Blueprint, render_template, url_for, request, current_app, redirect, flash
from flask_login import current_user, login_required, logout_user, login_user
from spalt.users.forms import SignupForm, LoginForm, AccountForm
from spalt import bcrypt, db
from spalt.users.spaltuns import ImageSave, ResetRequest
from spalt.models import User, Blogs
		
users = Blueprint('users', __name__)

@users.route('/', methods=['GET', 'POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('home.main'))
	form = LoginForm()
	if form.validate_on_submit():
		userlogininfo = request.form
		email = str(userlogininfo['email'])
		userpass = str(userlogininfo['password'])
		user = User.query.filter_by(email=email).first()
		if user and bcrypt.check_password_hash(user.password, userpass):
			login_user(user)
			flash("you've logged in successfully", 'success')
			forced_out_page = request.args.get('next')
			return redirect(forced_out_page) if forced_out_page else redirect(url_for('home.main'))
		else:
			flash("sorry log in unsuccessfully please check email and password", 'danger')
			return render_template('index.html', form=form)
	return render_template('index.html', form=form)

@users.route('/signup', methods=['GET', 'POST'])
def signup():
	if current_user.is_authenticated:
		return redirect(url_for('home.main'))
	form = SignupForm()
	if form.validate_on_submit():
		fullname = form.fullname.data.lower()
		username = form.username.data.capitalize()
		email = form.email.data
		password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')

		user = User.query.filter_by(email=email).first()
		if user:
			flash("Sorry email already exists", 'info')
			return render_template('signup.html', form=form)
		user_name = User.query.filter_by(username=username).first()
		if user_name:
			flash('Sorry username is taken exists', 'info')
			return render_template('signup.html', form=form)

		user = User(fullname=fullname, username=username, email=email, password=password)
		db.session.add(user)
		db.session.commit()
		login_user(user)

		user = User.query.filter_by(username=username).first()
		login_user(user)

		flash(f'Your account has been created successfully', 'success')
		return redirect(url_for('home.main'))
	return render_template('signup.html', form=form)


@users.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('users.login'))


@users.route('/account', methods=['POST', 'GET'])
@login_required
def account():
	form = AccountForm()
	if form.validate_on_submit():
		if form.image_file.data:
			picture_file =  ImageSave.saving_picture(form.image_file.data)
			current_user.imagefile = picture_file
		current_user.fullname = form.fullname.data
		current_user.email = form.email.data
		db.session.commit()
	elif request.method == 'GET':
		form.fullname.data = current_user.fullname
		form.email.data = current_user.email
	image_file = url_for('static', filename='profile_pics/' +
                        current_user.imagefile)
	return render_template ('account.html', image_file=image_file, form=form)


@users.route('/timeline/<string:username>')
@login_required
def user_timeline(username):
	user = User.query.filter_by(username=username).first_or_404()
	posts = Blogs.query.filter_by(author=user)
	return render_template('user_page.html', user=user, posts=posts, username=username)

@users.route('/reset_password', methods=['POST', 'GET'])
def reset_password_token():
	if current_user.is_authenticated:
		return redirect(url_for('home.main'))
	# token = ResetRequest.reset_token()
	return render_template('reset_request.html')

@users.route('/reset_password/<token>', methods=['POST', 'GET'])
def reset_password(token):
	if current_user.is_authenticated:
		return redirect(url_for('home.main'))
	user = ResetRequest.token_verifier(token)
	if form.validate_on_submit():
		password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
		user.password = password
		db.session.commit()
		flash('Your Password has been reset, you are now able to login', 'success')
		return redirect(url_for('login'))
	return render_template('reset_password.html')