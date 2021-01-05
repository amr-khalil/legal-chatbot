# models.py for Database models

# Import libraries 
from datetime import datetime
from app import db, login
from flask_login import UserMixin

# For password hashing
from hashlib import md5 
from werkzeug.security import generate_password_hash, check_password_hash

# Many-to-Many db relationship
followers = db.Table(
	'followers',
	db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
	db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))

	)

'''
User database model
The User class created above inherits from db.Model, a base class for all models from Flask-SQLAlchemy.
This class defines several fields as class variables.
'''
class User(UserMixin, db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(64), index=True, unique=True)
	email = db.Column(db.String(128), index=True, unique=True)
	password_hash = db.Column(db.String(128))
	posts = db.relationship('Post', backref='author', lazy='dynamic')
	about_me = db.Column(db.String(140), default='test')
	last_seen = db.Column(db.DateTime, default=datetime.utcnow)
	followed = db.relationship(
        'User', secondary=followers,
        primaryjoin=(followers.c.follower_id == id),
        secondaryjoin=(followers.c.followed_id == id),
        backref=db.backref('followers', lazy='dynamic'), lazy='dynamic')

	# The __repr__ method tells Python how to print objects of this class, which is going to be useful for debugging.
	def __repr__(self):
		return '<User {}>'.format(self.username)

	# Create hashed password for users
	def set_password(self, password):
		self.password_hash = generate_password_hash(password)

	# Password hashing and verification
	def check_password(self, password):
		return check_password_hash(self.password_hash, password)

	# Create user avatar
	def avatar(self, size):
		digest = md5(self.email.lower().encode('utf-8')).hexdigest()
		return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(digest, size)

	# Follow another users
	def follow(self, user):
		if not self.is_following(user):
			self.followed.append(user)

	# Unfollow another users
	def unfollow(self, user):
		if self.is_following(user):
			self.followed.remove(user)

	# Check if user A is already following user B
	def is_following(self, user):
		return self.followed.filter(followers.c.followed_id == user.id).count() > 0

	# Show posts form the followed users
	def followed_posts(self):
		followed =  Post.query.join(
			followers, (followers.c.followed_id == Post.user_id)).filter(
				followers.c.follower_id == self.id)
		return followed.union(self.posts).order_by(Post.timestamp.desc())

@login.user_loader
def load_user(id):
	return User.query.get(int(id))

'''
Post database model
The new Post class will represent blog posts written by users.
The timestamp field is going to be indexed, which is useful if you want to retrieve posts in chronological order. 
'''
class Post(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	body = db.Column(db.String(140))
	timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

	# For debugging
	def __repr__(self):
		return '<Post {}>'.format(self.body)		