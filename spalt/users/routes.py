from flask import Flask, render_template, redirect, flash, url_for, request
from flask_login import current_user, login_user, logout_user, login_manager
from users.forms import LoginForm, SignupForm
import bcrypt
from spalt import db, app
		

@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('mainrotes.main'))
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		if user and bcrypt.checkpw(form.password.data.encode('utf-8'), user.password):
			login_user(user, remember=remember.form.data)
			return render_template(url_for('index.html'))
		else :
			flash('login unsuccess full. please check email and password and try again', 'category')
	return render_template('userinfo/login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
	if current_user.is_authenticated:
		return render_template(url_for('index.html'))
	form = SignupForm()
	if form.validate_on_submit():
		hashpassword = bcrypt.hasspw(form.password.data.encode('utf-8'), gensalt())
		user = User(firstName=form.firstname.data, 
					lastName=form.lastname.data, 
					username=form.username.data, 
					email=form.email.data,
					password=hashpassword)
		session.db.add(user)
		session.db.commit()
		flash(f'Your account has been created successfully', 'success')
		return redirect(url_for('main'))
	return render_template('userInfo/signup.html', form=form)


@app.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('index.html'))