import os

class Config:
	SECRET_KEY = os.environ.get('SECRET_KEY')  or 'a7d244bea936fa2e710637630160ac4dcec246c8'
	SQLALCHEMY_DATABASE_URI = os.environ.get('SPALT_DB') and 'sqlite:///spalt.db'
	DEBUG = True
	
	# MAIL_SERVER = 'smtp.mail.yahoo.com'
	# MAIL_PORT = 465
	# MAIL_USE_TLS = True
	# MAIL_USERNAME = os.environ.get('USER_EMAIL')
	# MAIL_PASSWORD = os.environ.get('USER_PASSWORD')

class Deploy(Config):
	DEBUG = False
	SQLALCHEMY_DATABASE_URI = 'sqlite:///spalt.db'


		