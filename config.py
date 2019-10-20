import os
basedir = os.path.abspath(os.path.dirname(__file__))

'''
# Purpose

This script is designed simply to grab our secret_key for use in validating
forms and ensuring we are protected from CSRF attacks.

'''

class Config(object):
    SECRET_KEY = os.environ.get('QUOTEBOOK_SECRET')


    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') 
    SQLALCHEMY_TRACK_MODIFICATIONS = False
