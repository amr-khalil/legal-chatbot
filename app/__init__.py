# The __init__.py file is required to make Python treat the directories as containing packages

# Import libraries 
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_login import LoginManager
from flask_moment import Moment

# Create the application object as an instance of class Flask
app = Flask(__name__)
# Import app configrations from config.py
app.config.from_object(Config)
# Create SQL Alchemy database 
db = SQLAlchemy(app)
# Migrate the database
migrate = Migrate(app, db)
# Create login manager
login = LoginManager(app)
login.login_view = 'login'
# Moment for converting the server time to local user time
moment = Moment(app)

# Create flask admin panel
admin = Admin(app, name='Legal Chatbot', template_mode='bootstrap3')
from app import routes, models
# Add User aand Posts to flask admin panel
admin.add_view(ModelView(models.User, db.session))
admin.add_view(ModelView(models.Post, db.session))

