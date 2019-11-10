from . import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login

'''
The following classes spell out the db schema for flask to build/insert data into.
This is all spelled out in the model.xml file.
'''

class users(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    signup_datetime = db.Column(db.DateTime,index=True, default = datetime.utcnow)
    quotes = db.relationship('quotes',backref='submitted_by',lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self,password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash,password)

class people_quoted(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(32))
    last_name_initial = db.Column(db.String(1))
    quotes = db.relationship('quotes',backref='primary_person_quoted',lazy='dynamic')
    quote_phrases = db.relationship('phrases',backref='person_quoted',lazy='dynamic')

    def __repr__(self):
        return '<person_quoted {} {}>'.format(self.first_name,self.last_name_initial)

class quotes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    submitted_by_id = db.Column(db.Integer,db.ForeignKey('users.id'))
    primary_person_quoted_id = db.Column(db.Integer,db.ForeignKey('people_quoted.id'))
    submitted_datetime = db.Column(db.DateTime,index=True,default=datetime.utcnow)
    context = db.Column(db.String(140))
    phrases = db.relationship('phrases',backref='from_quote',lazy='dynamic')

    def __repr__(self):
        return "<quote {}, submitted_by {}, referencing {} at {}>".format(
            self.id,self.submitted_by_id,self.primary_person_quoted_id,self.submitted_datetime
        )

class phrases(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quote_id = db.Column(db.Integer,db.ForeignKey('quotes.id'))
    person_quoted_id = db.Column(db.Integer,db.ForeignKey('people_quoted.id'))
    phrase_text = db.Column(db.String(500))

    def __repr__(self):
        return 'phrase: "{}", - {}'.format(self.phrase_text,self.person_quoted_id)


@login.user_loader
def load_user(id):
    return users.query.get(int(id))
