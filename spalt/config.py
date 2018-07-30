class Config:
	SECRET_KEY = '3da8dfc5ed7003c124b7294ab73d31dda0b11c6b'
	SQLALCHEMY_DATABASE_URI = 'mysql://root:@localhost/spalt'
	
	MAIL_SERVER = 'smtp.mail.yahoo.com'
	MAIL_PORT = 465
	MAIL_USE_TLS = True
	MAIL_USERNAME = os.environ.get('USER_EMAIL')
	MAIL_PASSWORD = os.environ.get('USER_PASSWORD')