from . import db
from datetime import datetime
from time import time
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login,app
import jwt

'''
The following classes spell out the db schema for flask to build/insert data into.
This is all spelled out in the model.xml file.
'''

class users(UserMixin, db.Model):

    #schema
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    is_verified = db.Column(db.Boolean,  default = False)
    password_hash = db.Column(db.String(128))
    is_admin = db.Column(db.Boolean, default = False)
    signup_datetime = db.Column(db.DateTime,index=True, default = datetime.utcnow)

    #relationship
    quotes = db.relationship('quotes',backref='submitted_by',lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self,password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash,password)

    def check_admin_status(self):
        return self.is_admin

    def check_is_verified(self):
        return self.is_verified

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password':self.id, 'exp':expires_in+time()},
            app.config['SECRET_KEY'], algorithm='HS256').decode('utf-8')

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, app.config['SECRET_KEY'],
                            algorithms=['HS256'])['reset_password']
        except:
            return
        return users.query.get(id)

class people_quoted(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32))
    #quotes = db.relationship('quotes',backref='primary_person_quoted',lazy='dynamic')

    def __repr__(self):
        return '<person_quoted {}>'.format(self.name)

class quotes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date)
    phonetic_date = db.Column(db.String(32))
    submitted_by_id = db.Column(db.Integer,db.ForeignKey('users.id'))
    primary_person_quoted_id = db.Column(db.Integer,db.ForeignKey('people_quoted.id'))
    submitted_datetime = db.Column(db.DateTime,index=True,default=datetime.utcnow)
    context = db.Column(db.String(140))
    # phrases = db.relationship('phrases',backref='from_quote',lazy='dynamic')

    def __repr__(self):
        return "<quote {}, submitted_by {}, referencing {} at {}>".format(
            self.id,self.submitted_by_id,self.primary_person_quoted_id,self.submitted_datetime
        )

class phrases(db.Model):

    #schema
    id = db.Column(db.Integer, primary_key=True)
    quote_id = db.Column(db.Integer,db.ForeignKey('quotes.id'))
    person_quoted_id = db.Column(db.Integer,db.ForeignKey('people_quoted.id'))
    phrase_text = db.Column(db.String(500))

    #relationships
    quote = db.relationship('quotes',
                            backref=db.backref('phrases',
                                                lazy='dynamic',
                                                collection_class=list))
    person_quoted = db.relationship('people_quoted',
                                    backref=db.backref('phrases',
                                                lazy='dynamic',
                                                collection_class=list))


    def __repr__(self):
        return 'phrase: "{}", - {}'.format(self.phrase_text,self.person_quoted_id)


@login.user_loader
def load_user(id):
    return users.query.get(int(id))
