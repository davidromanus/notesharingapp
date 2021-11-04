from flask_wtf import FlaskForm 
from wtforms import TextField,IntegerField,TextAreaField,StringField,PasswordField,SubmitField,BooleanField
from wtforms.validators import DataRequired,Length,Email,EqualTo,ValidationError
from flask_wtf.file import FileField,FileAllowed
from app.models import User
from flask_login import current_user

class RegistrationForm(FlaskForm):
	username=StringField('Username',validators=[DataRequired(),Length(min=2,max=60)])
	picture=FileField('Update Profile picture',validators=[FileAllowed(['jpg','png','jpeg','jfif'])])
	field=StringField('Field',validators=[DataRequired()])
	address=TextField('address',validators=[DataRequired()])
	phone=IntegerField('Phone Number')
	password=PasswordField('Password',validators=[DataRequired(),Length(min=8,max=120)])
	submit=SubmitField('Submit')

	def validate_username(self,username):
		user=User.query.filter_by(username=username.data).first()
		if user is not None:
			raise ValidationError('please user a different username')

	def validate_number(self,number):
		user=User.query.filter_by(phoneNumber=phone.data).first()
		if user is not None:
			raise ValidationError('please user a different Phone Number')

class LoginForm(FlaskForm):
	username=StringField('Username',validators=[DataRequired(),Length(min=5,max=120)])
	password=PasswordField('Password',validators=[DataRequired(),Length(min=8,max=120)])
	submit=SubmitField('Submit')

class PostForm(FlaskForm):
	title=StringField('Title',validators=[DataRequired(),Length(min=2,max=200)])
	post=TextAreaField('mypost',validators=[Length(min=2,max=1000)])
	submit=SubmitField('post')


#the handlers for editing notes
class EditProfileForm(FlaskForm):
	username=TextField('username',validators=[DataRequired()])
	about=TextAreaField('about',validators=[DataRequired(),Length(min=2,max=150)])
	picture=FileField('Update Profile picture',validators=[FileAllowed(['jpg','png'])])
	submit=SubmitField('submit')

	def validate_username(self,username):
		if username.data != current_user.username:
			user=User.query.filter_by(username=username.data).first()
			if user:
				raise ValidationError('please user a different username')

	def validate_number(self,number):
		user=User.query.filter_by(phoneNumber=phone.data).first()
		if user is not None:
			raise ValidationError('please user a different Phone Number')



class EditPostForm(FlaskForm):
	title=StringField('Title',validators=[DataRequired(),Length(min=2,max=200)])
	post=TextAreaField('My Post',validators=[Length(min=2,max=150)])
	submit=SubmitField('Update Post')