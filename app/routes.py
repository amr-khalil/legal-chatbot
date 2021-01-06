# routes.py returns the complete HTML pages from view function
# Import libraries 
from app import app
from flask import render_template, redirect, request, url_for, flash, session
from werkzeug.urls import url_parse
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import current_user, login_user, logout_user, login_required
import os
from app import db
from app.models import User, Post
from app.algorithm import search_FAQ, web_mining
import pandas as pd

# Last seen function
@app.before_request
def before_request():
	if current_user.is_authenticated:
		current_user.last_seen = datetime.utcnow()
		db.session.commit()

# Route for home page
@app.route('/', methods=['POST', 'GET'])
@app.route('/index', methods=['POST', 'GET'])
def index():
	if request.method == 'POST' :
		question = request.form['question']
		url = '#'
		# FAQ is dataframe we must use iloc
		answer1, score = search_FAQ([question]).iloc[0][2], search_FAQ([question]).iloc[0][3]
		answer2 =  web_mining(question)
		#answer, score = search_FAQ([question]).iloc[0][2] or web_mining(question)
		answer = answer1 or answer2
		# If the answet not in FAQ list give 50% accuracy
		if score < 0.5:
			score = 50
		else:
			score = int(round(score, 2)*100)

		if 'question' in session:
			session['question'] += [question]
			session['answer'] +=[answer]
			session['score'] +=[score]
		else:
			session['question'] =[question]
			session['answer'] =[answer]
			session['score'] =[score]

		posts = [x for x in zip(session['question'], session['answer'],session['score'])][::-1]
		
		return render_template('index.html', posts = posts)

	return render_template('index.html')

# Route for login
@app.route('/login', methods=['POST','GET'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('index'))

	
	if request.method == 'POST' and request.form['username_email'] and request.form['password']:
		remember_me = True if request.form.get('remember_me') else False
		print(remember_me)

		username_email = request.form['username_email']
		password = request.form['password']
		
		user = User.query.filter_by(username=username_email).first() or User.query.filter_by(email=username_email).first()
		
		if user is None or not user.check_password(password):
			flash("{}".format(user))
			return redirect(url_for('login'))

		# Log the user in
		login_user(user, remember=remember_me)
		next_page = request.args.get('next')
		if not next_page or url_parse(next_page).netloc != '':
			next_page = url_for('index')

		return redirect(url_for('index'))
	return render_template('login.html')


# Route for registration
@app.route('/register', methods=['POST', 'GET'])
def register():
	# If request is correct
	if request.method == 'POST' and request.form['username'] and request.form['email'] and request.form['password'] and request.form['confirm_password']:
		username = request.form['username']
		email = request.form['email']
		password = request.form['password']
		confirm_password = request.form['confirm_password']

		# Check password matching
		if password != confirm_password:
			flash('Password is not matching')
			return render_template('register.html')

		# Check in if username or email in database
		check_username = User.query.filter_by(username=username).first()
		check_email = User.query.filter_by(email=email).first()

		if check_username is not None:
			flash('Username is already used')
			return render_template('register.html')

		if check_email is not None:
			flash('Email is already used')
			return render_template('register.html')

		# Then add new user and password
		new_user = User(username=username, email=email)
		new_user.set_password(password)
		db.session.add(new_user)
		db.session.commit()
		# add the new user to the database
		# If the inputs is ok open the login page
		return redirect(url_for('login'))
	return render_template('register.html')

# Route for user profile
@app.route('/user/<username>')
@login_required
def user(username):
	user = User.query.filter_by(username= username).first_or_404()
	page = request.args.get('page', 1, type=int)

	posts = Post.query.order_by(Post.timestamp.desc()).paginate(page, app.config['POSTS_PER_PAGE'], False)
	next_url = url_for('user', username=user.username, page=posts.next_num) if posts.has_next else None
	prev_url = url_for('user', username=user.username, page=posts.prev_num) if posts.has_next else None

	return render_template('user.html', user=user, posts=posts.items, 
		next_url=next_url, prev_url=prev_url)

# Route for Edit profile
@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
	if request.method == 'POST' and request.form['about_me']:
		current_user.about_me  = request.form['about_me']
		db.session.commit()
		flash('Your changes have been saved')
		return redirect(url_for('edit_profile'))
	elif request.method == 'GET':
		request.form['about_me'] = current_user.about_me

	return render_template('edit_profile.html')

# Route for Follow view
edit_profile
@app.route('/follow/<username>')
@login_required
def follow(username):
	user = User.query.filter_by(username=username).first()
	if user is None:
		flash('User {} not found'.format(username))
		return redirect(url_for('index'))
	if user == current_user:
		flash('You cannot follow yourself')
		return redirect(url_for('user', username=username))
	current_user.follow(user)
	db.session.commit()
	flash('You are now following {}'.format(username))
	return redirect(url_for('user', username=username))

# Route for Unfollow view
@app.route('/unfollow/<username>')
@login_required
def unfollow(username):
	user = User.query.filter_by(username=username).first()
	if user is None:
		flash('User {} not found'.format(username))
		return redirect(url_for('index'))
	if user == current_user:
		flash('You cannot unfollow yourself')
		return redirect(url_for('user', username=username))
	current_user.unfollow(user)
	db.session.commit()
	flash('You are not following {}'.format(username))
	return redirect(url_for('user', username=username))

# Route for logout
@app.route('/logout')
@login_required
def logout():
	logout_user()
	return redirect(url_for('login'))

# Route for Chatbot
@app.route('/chatbot')
#@login_required
def chatbot():
	return render_template('chatbot.html')

# Route for Voice Assistant
@app.route('/voice_assistant')
#@login_required
def voice_assistant():
	return render_template('voice_assistant.html')

# Route for software architecture
@app.route('/so_funktioniert_es')
#@login_required
def so_funktioniert_es():
	return render_template('so_funktioniert_es.html')
