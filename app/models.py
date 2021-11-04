from datetime import datetime
from app import db,Lm
from flask_login import UserMixin 

@Lm.user_loader
def load_user(id):
	return User.query.get(int(id))


class User(db.Model,UserMixin):
	id=db.Column(db.Integer,primary_key=True)
	username=db.Column(db.String,unique=True,nullable=False)
	address=db.Column(db.String,nullable=False)
	image_file=db.Column(db.String(20),nullable=False,default='default.jpg')
	field=db.Column(db.String,nullable=False,default='none')
	password=db.Column(db.String(100),nullable=False)
	about=db.Column(db.String(200))
	phoneNumber=db.Column(db.Integer,unique=1,nullable=1)
	last_seen=db.Column(db.DateTime,default=datetime.utcnow)
	posts=db.relationship('Post',backref='author',lazy="dynamic")


	def __repr__(self):
		return f'User("{self.username}","{self.location}")'


class Post(db.Model):
	id=db.Column(db.Integer,primary_key=True)
	title=db.Column(db.String(200),nullable=False)
	content=db.Column(db.Text,nullable=False)
	pub_date=db.Column(db.DateTime,nullable=False,default=datetime.utcnow)
	user_id=db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)

	def __repr__(self):
		return f'Post("{self.content}","{self.pub_date}")'
