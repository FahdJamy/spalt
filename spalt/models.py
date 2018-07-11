from spalt import db, login_manager, mysql
from flask_login import UserMixin


# handles sessions
@login_manager.user_loader
def load_user(user_id):
	User.query.get(int(user_id))

# @login_manager.user_loader
# def load_a_user(user_id):


# UserMixin help in session handlin' including. is user active, user annonymous, is user authenticated
class User(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key=True)
	fullname = db.Column(db.String(50), nullable=False)
	username = db.Column(db.String(30), nullable=False, unique=True)
	email = db.Column(db.String(120), nullable=False, unique=True)
	password = db.Column(db.String(60), nullable=False)
	imagefile = db.Column(db.String(12), nullable=False, default='default.jpg')

	# what the db returns
	def __repr__(self):
		return f"User('{self.fullname}', '{self.username}', '{self.email}', '{self.password}', '{self.imagefile}')"


# class Mysql(object):
#     # __instance = None

#     # __host = None
#     # __user = None
#     # __password = None
#     # __database = None

#     # __session = None
#     # __connection = None
	# from spalt import mysql
 #    cur = mysql.connection.cursor()
 #    result = cur.execute("SELECT * FROM userinfo")

    # def __new__(cls, *args, **kwargs):
    #     if not cls.__instance:
    #         cls.__instance = super(Mysql, cls).__new__(cls, *args, **kwargs)
    #     return cls.__instance

    # def __init__(self, host='localhost', user='root', password='', database=''):
    #     self.__host = host
    #     self.__user = user
    #     self.__password = password
    #     self.__database = database



    #Open connection with database
    # def _open(self):
    #     try:
    #         cnx = mysql.connector.connect(host=self.__host, user=self.__user, password=self.__password,
    #                                       database=self.__database)
    #         self.__connection = cnx
    #         self.__session = cnx.cursor()
    #     except mysql.connector.Error as err:
    #         if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
    #             print ('Something is wrong with your user name or password')
    #         elif err.errno == errorcode.ER_BAD_DB_ERROR:
    #             print ('Database does not exists')
    #         else:
    #             print (err)

    # def _close(self):
    #     self.__session.close()
    #     self.__connection.close()

    # def insert(self, table, *args, **kwargs):
    #     values = None
    #     query = "INSERT INTO %s " % table
    #     if kwargs:
    #         keys = kwargs.keys()
    #         values = kwargs.values()
    #         query += "(" + ",".join(["`%s`"]*len(keys)) % tuple(keys) + ") VALUES(" + ",".join(["%s"]*len(values)) + ")"
    #     elif args:
    #         values = args
    #         query += " VALUES(" + ",".join(["%s"]*len(values)) + ")"
    #     self._open()
    #     self.__session.execute(query, values)
    #     self.__connection.commit()
    #     self._close()
    #     return self.__session.lastrowid

    # def select(self, table, where=None, *args):
    #     result = None
    #     query = "SELECT "
    #     keys = args
    #     l = len(keys) - 1
    #     for i, key in enumerate(keys):
    #         query += "`"+key+"`"
    #         if i < l:
    #             query += ","
    #     query += " FROM %s" % table
    #     if where:
    #         query += " WHERE %" % where
    #     self._open()
    #     self.__session.execute(query)
    #     self.__connection.commit()
    #     for result in self.__session.stored_results():
    #         result = result.fetchall()
    #     self._close()
    #     return result

    # def update(self, table, index, **kwargs):
    #     query = "UPDATE %s SET" % table
    #     keys = kwargs.keys()
    #     values = kwargs.values()
    #     l = len(keys) - 1
    #     for i, key in enumerate(keys):
    #         query += "`"+key+"`=%s"
    #         if i < l:
    #             query += ","
    #     query += " WHERE index=%d" % index
    #     self._open()
    #     self.__session.execute(query, values)
    #     self.__connection.commit()
    #     self._close()

    # def delete(self, table, index):
    #     query = "DELETE FROM %s WHERE uuid=%d" % (table, index)
    #     self._open()
    #     self.__session.execute(query)
    #     self.__connection.commit()
    #     self._close()

    # def call_store_procedure(self, name, *args):
    #     result_sp = None
    #     self._open()
    #     self.__session.callproc(name, args)
    #     self.__connection.commit()
    #     for result in self.__session.stored_results():
    #         result_sp = result.fetchall()
    #     self._close()
    #     return result_sp