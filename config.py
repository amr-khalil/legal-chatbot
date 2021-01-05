# App configrations
import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    # Data encryption 
    SECRET_KEY = os.environ.get('SECRET_KEY') or '*********'  
    # Database 
    SQLALCHEMY_DATABASE_URI = 'postgres://cqetmnwtscwkma:a4158dfd4adfe6374ac58ac3a2783a4213220dfdc02b00c7d502932f1b5715d8@ec2-54-216-202-161.eu-west-1.compute.amazonaws.com:5432/d2i2ieck1govpj'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Pagination
    POSTS_PER_PAGE = 25
