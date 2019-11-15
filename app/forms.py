from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo,ValidationError
from app.models import users

class LoginForm(FlaskForm):
    '''
    Build a class for forms so we can ask users who they are, to login,
    and to have the option to remember who they are next time
    they visit the site.
    '''

    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    email = StringField("Email Address",validators=[DataRequired()])
    password = StringField("Password", validators=[DataRequired()])
    password_validator = StringField('Confirm Password',
            validators=[DataRequired(),EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = users.query.filter_by(username=username.data).first()
        if user!=None:
            raise ValidationError('Try a different username. That one is used already.')

    def validate_email(self, email):
        user = users.query.filter_by(email=email.data).first()
        if user != None:
            raise ValidationError('Please use a different email address. That is used already.')

class VerifyUserForm(FlaskForm):
    verify = SubmitField(label='Verify User')
