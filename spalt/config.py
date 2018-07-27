import os

class Config:
	# generate random character Secrety key, this is done in the cmdline
	SECRET_KEY = '9c4a536d605db74aad943b64c3adb011' #one that will be used so as 4 our cookies used for keeping users logged in not termpered w/
	SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db' #this db will be created in our directory alongside our py module that we in
	# set come constants here 4 how our app will know how 2 send mail
	MAIL_SERVER = 'smtp.mail.yahoo.com'
	MAIL_PORT = 465
	MAIL_USE_TLS = True
	MAIL_USERNAME = os.environ.get('USER_EMAIL')
	MAIL_PASSWORD = os.environ.get('USER_PASSWORD')