from datetime import datetime
from flask import render_template,redirect,url_for,flash,request
from app import app,db,bc
from .forms import RegistrationForm,LoginForm,PostForm,EditProfileForm,EditPostForm
from .models import User,Post
from flask_login import login_user,current_user,logout_user,login_required
from werkzeug.urls import url_parse
import os
from app.utils import save_picture




@app.before_request
def before_request():
	if current_user.is_authenticated:
		current_user.last_seen=datetime.utcnow()
		db.session.commit()

#----------authentication starts here
@app.route('/register',methods=['POST','GET'])
def register():
	if current_user.is_authenticated:
		return redirect(url_for('index'))
	form=RegistrationForm()
	if form.validate_on_submit():
		hp=bc.generate_password_hash(form.password.data).decode('utf-8')
		user=User(username=form.username.data,
			address=form.address.data,field=form.field.data,phoneNumber=form.phone.data,
			password=hp)
		db.session.add(user)
		db.session.commit()
		flash(f'your account has been created','success')
		return redirect('index')
	return render_template('register.html',
		form=form,
		title='sign in')


@app.route('/login',methods=['POST','GET'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('index'))
	form=LoginForm()
	if form.validate_on_submit():
		user=User.query.filter_by(username=form.username.data).first()
		if user and bc.check_password_hash(user.password,form.password.data):
			login_user(user)
			return redirect(url_for('index'))
		if user is None or not user.username:
			flash('invalid usernameor password',
				'danger')
		next_page=request.args.get('next')
		if not next_page or url_parse(next_page).netloc !='':
			next_page=url_for('login')
		return redirect(next_page)
	return render_template('login.html',
		form=form,
		title='login ')



@app.route('/logout')
@login_required
def logout():
	logout_user()
	return redirect(url_for('index'))


#----------authentication stops here

@app.route('/account/<username>')
@login_required
def account(username):
	user=User.query.filter_by(username=username).first()
	post=Post.query.filter_by(user_id=current_user.id).order_by(Post.pub_date.desc()).all()
	image_file=url_for('static',filename='profile_pics/' + user.image_file)
	return render_template('account.html',
		user=user,
		post=post,
		title='profile',
		image_file=image_file)




@app.route('/')
@app.route('/index/')
def index():
	notes=Post.query.order_by(Post.pub_date.desc()).all()
	return render_template('index.html',notes=notes)




@app.route('/make_post',methods=['POST','GET'])
@login_required
def create_note():
	form=PostForm()
	if form.validate_on_submit():
		post=Post(title=form.title.data,content=form.post.data,author=current_user)
		db.session.add(post)
		db.session.commit()
		flash('posted','success')
		return redirect(url_for('create_note'))
	return render_template('create_post.html',form=form)


@app.route('/read/<int:id>',methods=['POST','GET'])
@login_required
def read(id):
	note=Post.query.get_or_404(id)
	return render_template('read.html',note=note)


#editing sections:all editings will be handled here

@app.route('/edit_profile/',methods=['POST','GET'])
@login_required
def edit_profile():
	form=EditProfileForm()
	if form.validate_on_submit():
		if form.picture.data:
			picture_file=save_picture(form.picture.data)
			current_user.image_file=picture_file
		current_user.username=form.username.data
		current_user.about=form.about.data
		db.session.commit()
		flash('your  profile has been updated.','success')
		return redirect(url_for('user.account',
			username=current_user.username,
			about=current_user.about)
		)
	elif request.method=='GET':
	    form.username.data=current_user.username
	    form.about.data=current_user.about
	return render_template('edit_profile.html',form=form)



@app.route('/edit_post/<int:id>',methods=['POST','GET'])
@login_required
def edit_post(id):
	form=EditPostForm()
	note_to_edit=Post.query.get_or_404(id)

	if request.method=='POST':
		note_to_edit.title=form.title.data
		note_to_edit.content=form.post.data
		db.session.commit()
		flash('updated successfully','success')
		return redirect(url_for('index',
			sub_title=note_to_edit.title,
			content=note_to_edit.content))
	elif request.method=='GET':
		form.title.data=note_to_edit.title
		form.post.data=note_to_edit.content
	return render_template('edit-post.html',form=form)


@app.route('/delete/<int:id>')
@login_required
def delete(id):
	note_to_delete=Post.query.get_or_404(id)
	db.session.delete(note_to_delete)
	db.session.commit()
	flash('deleted','danger')
	return redirect(url_for('index'))
#editing ends here