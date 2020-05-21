import os

'''
# Purpose

This script is designed simply to grab our secret_key for use in validating
forms and ensuring we are protected from CSRF attacks.

'''

class Config(object):
    SECRET_KEY = os.environ.get('QUOTEBOOK_SECRET')


    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    QUOTES_PER_PAGE = 6
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    ADMINS = ['nicolesquotebook@gmail.com']
