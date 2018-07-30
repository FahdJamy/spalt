import os
import secrets
from PIL import Image
from spalt.models import User, Blogs
from flask import current_app
from itsdangerous import TimedJSONWebSignatureSerializer as TokenSeri

class ImageSave:
	def saving_picture(form_picture):
		file_name_token = secrets.token_hex(7)
		_, f_ext = os.path.splitext(form_picture.filename)
		image_name = str(file_name_token + f_ext)
		file_path = os.path.join(current_app.root_path, 'static/profile_pics', image_name)

		resized_size = (200, 200)
		image_resized = Image.open(form_picture)
		image_resized.thumbnail(resized_size)

		image_resized.save(file_path)
		return image_name


class ResetRequest:
	def reset_token():
		seconds_to_expire = 1800
		token_serializer = TokenSeri(current_app.config['SECRET_KEY'], seconds_to_expire)
		token = token_serializer.dumps({'user_id': User.id}).decode('utf-8')
		return token

	def token_verifier(token):
		token_serializer = TokenSeri(current_app.config['SECRET_KEY'])
		try:
			user_id = token_serializer.loads(token).user_id		
		except:
			None

		user = User.query.get(user_id)
		return user
	def password_email_sender(user):
		pass
		