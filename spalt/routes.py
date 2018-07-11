import os
import secrets
from PIL import Image
from flask import Flask, render_template, redirect, flash, url_for, request, session, g
from flask_login import current_user, login_user, logout_user, login_required, UserMixin
from spalt.forms import LoginForm, SignupForm, PostForm, AccountForm, MysqlResults
from spalt.models import User
from wtforms.validators import ValidationError
import bcrypt
from spalt import db, app, mysql, login_manager, bcrypt
from functools import wraps

ForumType = ['Sports', 'Educational', 'Business', 'Economic', 'Money', 'Business', 'Technology']

# checking wehther user is logged in
def login_require(f):
	@wraps(f)
	def wrap(*args, **kwargs):
		if 'logged_in' in session:
			return f(*args, **kwargs)
		else:
			flash('Unauthorized, please login first', 'danger')
			return redirect(url_for('login'))
	return wrap

@login_manager.user_loader
def load_user(user_id):
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

@app.route('/', methods=['GET', 'POST'])
def login():
	# if current_user.is_authenticated:
	# 	return redirect(url_for('main'))
	form = LoginForm()
	if request.method == 'POST':
		session.pop('user', None)

		userlogininfo = request.form
		email = str(userlogininfo['email'])
		userpass = str(userlogininfo['password'])

		email_db = MysqlResults.email_returner(str(email))
		dbpass = MysqlResults.password_returner(email)

		if email_db == email:

			if bcrypt.check_password_hash(dbpass, userpass):
				user_logged_in = MysqlResults.user_returner(email)
			# session['logged_in'] = True
			# session['username'] = email
				# login_user(user_logged_in)
				session['user'] = user_logged_in
				# forced_out_page = request.args.get('next')
				flash("you've logged in successfully", 'success')
				# return redirect(forced_out_page) if forced_out_page else 
				return redirect(url_for('main'))

	return render_template('index.html', form=form)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
	if current_user.is_authenticated:
		return render_template(url_for('main'))
	form = SignupForm()
	if form.validate_on_submit():
		fullname = form.fullname.data
		username = form.username.data
		email = form.email.data
		password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')

		cur = mysql.connection.cursor()
		result = cur.execute("SELECT * FROM userinfo where email = %s", [email])
		if result > 0:
			undata = cur.fetchone()
			usernamedt = undata['username']
			emaildt = undata['email']
			cur = mysql.connection.cursor()
			if usernamedt == username:
				flash(f'Sorry username is alredy taken please choose another username', 'danger')
				return redirect(url_for('signup'))
			elif emaildt:
				flash(f'Sorry email is alredy taken please choose another email', 'danger')
				return redirect(url_for('signup'))

		cur.execute("INSERT into userinfo(fullname, username, email, password) VALUES(%s, %s, %s, %s)", 
				(fullname, username, email, password))
		mysql.connection.commit()
		cur.close()

		flash(f'Your account has been created successfully', 'success')
		session['user'] = username
		return redirect(url_for('main'))
	return render_template('signup.html', form=form)

@app.route('/main')
# @login_required
def main():
	if g.user:
		return render_template('home.html')

	return redirect(url_for('login'))

@app.route('/posts', methods=['GET', 'POST'])
# @login_required
def posts():
	form = PostForm()
	if form.validate_on_submit():
		title = form.title.data
		content = form.content.data
		forum = form.content.data

		cur = mysql.connection.cursor()
		cur.execute("INSERT INTO forum(title, content, author, forumtype) VALUES (%s, %s, %s)", 
					(title ,content, session['username'], forum))
		mysql.connection.commit()
		cur.close()
	return render_template('createpost.html', form=form)

@app.route('/logout')
# @login_require
def logout():
	# logout_user()
	session.pop('user', None)
	return redirect(url_for('login'))

@app.before_request
def before_request():
	g.user = None
	if 'user' in session:
		g.user = session['user']

def saving_picture(form_picture):
	file_toke = secrets.token_hex(9)
	_, file_xt = os.path.splitext(form_picture)
	image_name = file_toke + file_xt
	file_path = os.path.join(app.root_path, 'static/profile_pics', image_name)

	resized_size = (300, 300)
	image_resized = Image.open(form_picture)
	image_resized.thumbnail(resized_size)

	image_resized.save(file_path)
	return image_name


@app.route('/account')
def account():
	form = AccountForm()
	if form.validate_on_submit():
		if form.image_file.data:
			picture_file = saving_picture(form.picture.data)
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