# App configrations
import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    # Data encryption 
    SECRET_KEY = os.environ.get('SECRET_KEY') or '*********'  
    # Database 
    SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'chatbot.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Pagination
    POSTS_PER_PAGE = 25
