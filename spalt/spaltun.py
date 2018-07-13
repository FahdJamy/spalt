import os
import secrets
from flask import flash, redirect, render_template, url_for
from PIL import Image
from flask_login import UserMixin
from spalt import db
from spalt.models import User, Blogs

class ImageSave:

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

class MysqlResults(UserMixin):
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

		