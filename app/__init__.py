from flask import Flask
from flask_sqlalchemy import SQLAlchemy 
from flask_bcrypt import Bcrypt 
from flask_login import LoginManager



app=Flask(__name__)
app.config['SECRET_KEY']='development'
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///database.db'
db=SQLAlchemy(app)
bc=Bcrypt(app)
Lm=LoginManager(app)
Lm.login_view='login'


from app import routes,models