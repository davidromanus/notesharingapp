#configuration file
import os
#from . import create_app


class Config(object):
	SECRET_KEY='thisismysecretkey'
	SQLALCHEMY_DATABASE_URI='sqlite:///database.db'
	SQLALCHEMY_TRACK_MODIFICATIONS=True