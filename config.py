from app.env import env

'''
Uses environment variables to secure secrets whilst giving our server the ability to 
access certain key parameters for things like emailing users managing csrf tokens. 

'''

class Config(object):
    SECRET_KEY = env.SECRET_KEY
    DATABASE_USER = env.DATABASE_USER
    DATABASE_PASSWORD = env.DATABASE_PASSWORD
    SQLALCHEMY_DATABASE_URI = 'postgresql://{username}:{password}@quotebookdb.crrajmxjcrsc.us-east-2.rds.amazonaws.com:5432/postgres'.format(username = DATABASE_USER, password = DATABASE_PASSWORD)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    QUOTES_PER_PAGE = 6
    MAIL_SERVER = env.MAIL_SERVER
    MAIL_PORT = int(env.MAIL_PORT or 25)
    MAIL_USE_TLS = env.MAIL_USE_TLS is not None
    MAIL_USERNAME = env.MAIL_USERNAME
    MAIL_PASSWORD = env.MAIL_PASSWORD
    ADMINS = ['nicolesquotebook@gmail.com']
