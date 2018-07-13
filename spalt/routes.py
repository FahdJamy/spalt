from flask import Flask, render_template, redirect, flash, url_for, request, session
from flask_login import current_user, login_user, logout_user, login_required
from spalt.forms import LoginForm, SignupForm, PostForm, AccountForm
from spalt.models import User, Blogs
import bcrypt
from spalt import db, app, mysql, login_manager, bcrypt
from spalt.spaltun import ImageSave

ForumType = ['Sports', 'Educational', 'Business', 'Economic', 'Money', 'Business', 'Technology']

@app.route('/', methods=['GET', 'POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('main'))
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
			return redirect(forced_out_page) if forced_out_page else redirect(url_for('main'))
		else:
			flash("sorry log in unsuccessfully please check email and password", 'danger')
			return render_template('index.html', form=form)
	return render_template('index.html', form=form)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
	if current_user.is_authenticated:
		return redirect(url_for('main'))
	form = SignupForm()
	if form.validate_on_submit():
		fullname = form.fullname.data
		username = form.username.data
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
		return redirect(url_for('login'))
	return render_template('signup.html', form=form)

@app.route('/main')
@login_required
def main():
	return render_template('home.html')

@app.route('/posts', methods=['GET', 'POST'])
@login_required
def posts():
	form = PostForm()
	if form.validate_on_submit():
		title = form.title.data
		content = form.content.data
		forum = form.content.data
	return render_template('createpost.html', form=form)

@app.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('login'))

@app.route('/account')
@login_required
def account():
	form = AccountForm()
	if form.validate_on_submit():
		if form.image_file.data:
			picture_file =  ImageSave.saving_picture(form.picture.data)
			current_user.image_file = picture_file
		email = form.email.data
		current_user.fullname = form.fullname.data
		current_user.username = form.username.data
		current_user.email = form.email.data
		cur = mysql.connection.cursor()
		user = cur.fetchone()
		user_id = user['id']
		cur.execute("UPDATE userinfo(username, email) VALUES (%s, %s, %s) where email = %s", [user_id])
	image_file = url_for('static', filename='profile_pics/default.jpg')
	return render_template ('account.html', image_file=image_file, form=form)