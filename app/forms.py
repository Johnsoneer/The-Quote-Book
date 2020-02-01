from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, FormField, DateTimeField,FieldList, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo,ValidationError,length
from wtforms import Form
from app.models import users
from datetime import datetime

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
    '''
    Form to register new users. Called in signup.html
    '''
    username = StringField("Username", validators=[DataRequired()])
    email = StringField("Email Address",validators=[DataRequired()])
    password = StringField("Password", validators=[DataRequired()])
    password_validator = StringField('Confirm Password',
                        validators=[DataRequired(),
                        EqualTo('password')])
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
    '''
    Form to verify the user for an admin.
    '''
    verify = SubmitField(label='Verify User')

class phraseForm(Form):
    '''
    Subform of Quote form. Creates a new unique phrase for each speaker.
    '''
    quoted_person_name = StringField("Person Quoted",validators = [DataRequired(),length(min=3,max=16)])
    phrase_text = TextAreaField('What Did They Say?', validators= [DataRequired(), length(max=500)])

class SubmitQuoteForm(FlaskForm):
    '''
    Form object for the Submit page. This form requests information from the user that turns into a new quote.
    '''

    phrases = FieldList(FormField(phraseForm),
                        min_entries=1,
                        max_entries=20)
    context = TextAreaField("Any context worth mentioning? (optional)")
