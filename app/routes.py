from flask import render_template, flash, redirect,  url_for,request
from flask_login import current_user, login_user, logout_user,login_required
from flask_paginate import Pagination, get_page_parameter, get_page_args
from werkzeug.urls import url_parse
from app.forms import LoginForm, RegistrationForm, VerifyUserForm, SubmitQuoteForm
from app import app,db
from app.models import users,people_quoted, quotes,phrases
import pandas as pd
import time


'''
This is the main script for executing the flask functions so we can
send our html templates to the browser for rendering. We boot, handle requests,
and configure our server right here.

Read more about Flask how-to here:
https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world
'''

def verify_administrator(username):
    '''
    Quick function to verify a user and, if they fail, boot them back to the home page.
    '''
    user = users.query.filter_by(username=username).first_or_404()
    is_admin = user.is_admin
    if is_admin ==False:
        flash("You are not an administrator. Quit trying to access the \
        admin panel!")
        return redirect(url_for('home'))
    return is_admin

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/about/')
@login_required
def about():
    return render_template('about.html',title='About')

@app.route('/login/',methods=['GET',"POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = users.query.filter_by(username=form.username.data).first()
        if user== None:
            flash("Huh. That username isn't in the database anywhere. Try a different one.")
            return redirect(url_for('login'))
        elif not user.check_password(form.password.data):
            flash("Poop. That password doesn't match the username." )
            return redirect(url_for('login'))
        elif not user.check_is_verified():
            flash("Looks like you haven't been verified yet. You'll need to be\
            verified by a site administrator before you can fully log in.")
            return redirect(url_for('login'))
        else:
            login_user(user, remember=form.remember_me.data)
            next_page = request.args.get('next')
            if not next_page or url_parse(next_page).netloc != '':
                next_page = url_for('home')
            return redirect(next_page)
    return render_template('login.html',title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = users(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("Your submission has been sent. But you'll have to have an \
        administrator verify before you can log in.")
        return redirect(url_for('login'))
    return render_template('signup.html', title='Signup', form=form)

@app.route('/admin_verify/<username>', methods=['GET','POST'])
@login_required
def admin_verify(username):
    if verify_administrator(username):

        # pull all user data for verification
        user_data_raw = users.query.all()
        data = {'current_user':current_user,
                'table':user_data_raw}

        return render_template('admin_verify.html',
                                title = 'Administrator Panel: Verify Users',
                                data = data)

@app.route('/admin_manage/<username>', methods=['GET','POST'])
@login_required
def admin_manage(username):
    if verify_administrator(username):
        data = {}
        # pull all quotes and their phrases for deletion if necessary.
        quotes_data =  quotes.query.all()
        phrases_data = phrases.query.all()
        people_quoted_data = people_quoted.query.all()
        phrases_df = pd.DataFrame([[x.quote_id,x.phrase_text] for x in phrases_data])
        phrases_df.columns = ['quote_id','phrases']
        quotes_df  = pd.DataFrame([[x.primary_person_quoted_id,x.id,x.submitted_datetime] for x in quotes_data])
        quotes_df.columns = ['person_quoted','quote_id','submission_date']
        people_quoted_df = pd.DataFrame([[x.id,x.name] for x in people_quoted_data])
        people_quoted_df.columns = ['person_quoted','name']
        quotes_df = quotes_df.merge(people_quoted_df,
                              on='person_quoted',
                              how='inner')
        data['quotes'] = quotes_df.merge(phrases_df.groupby('quote_id').sum().reset_index(),
                            on='quote_id',
                            how='inner')
        data['current_user'] = current_user
        return render_template('admin_manage.html',
                                title = 'Administrator Panel: Manage',
                                data = data)

@app.route('/verify_user/<username>/<verify_username>', methods=['GET','POST'])
@login_required
def verify_user(username,verify_username):
    if verify_administrator(username):

        user_to_verify = users.query.filter_by(username=verify_username).first()
        user_to_verify.is_verified = True
        db.session.add(user_to_verify)
        db.session.commit()

        return redirect(url_for('/admin_verify/{}'.format(user.username)))

@app.route('/delete_quote/<username>/<quote_id>', methods=['GET','DELETE','POST'])
@login_required
def delete_quote(username,quote_id):
    if verify_administrator(username):

        del_quote = quotes.query.filter_by(id = quote_id).all()
        del_phrases = phrases.query.filter_by(quote_id = quote_id).all()
        for qt in del_quote:
            for phr in del_phrases:
                db.session.delete(phr)
            db.session.delete(qt)
        db.session.commit()
    time.sleep(2)
    return redirect(url_for('admin_manage',username=username))





@app.route('/submit', methods=['POST','GET'])
@login_required
def submit():
    #create the forms and data to send to the page
    submit_form = SubmitQuoteForm()
    people = people_quoted.query.all()
    people = [x.name for x in people]
    submitting_user =  current_user.id
    quoted_in_session = []
    if submit_form.validate_on_submit():

        #submit context with new quote object
        if submit_form.context:
            new_quote = quotes(submitted_by_id=submitting_user,
                                context = submit_form.context.data)
        else:
            new_quote = quotes(submitted_by_id=submitting_user)

        # add phrases to quote object
        for phrase in submit_form.phrases:
            person = phrase.quoted_person_name.data
            person_lower = person.lower()
            people_list = [str(x).lower() for x in people]


            # add new person_quoted if necessary
            if person_lower not in people_list:
                person_to_add = people_quoted(name=person)
                db.session.add(person_to_add)
                db.session.commit()
                person_quoted_id = person_to_add.id
                people_list.append(person_lower)
            else:
                person_quoted_id = people_quoted.query.filter_by(name=person).first_or_404().id

            new_phrase = phrases(phrase_text = phrase.phrase_text.data,
                                person_quoted_id = person_quoted_id)
            new_quote.phrases.append(new_phrase)
            quoted_in_session.append(person_quoted_id)

        # whoever spoke last is the primary person quoted
        new_quote.primary_person_quoted_id = quoted_in_session[-1]
        new_quote.date = submit_form.quote_date.data
        #add form data to the database
        db.session.add(new_quote)
        db.session.commit()

        flash("Successfully submitted quote! View it on the 'Quotes' page!" )
        return redirect(url_for('submit'))
    return render_template('submit.html', title = 'Submit',
                        people = people, form = submit_form)


@app.route('/quote')
@login_required
def quote_page():

    page = request.args.get(get_page_parameter(), type=int, default=1)
    per_page = app.config['QUOTES_PER_PAGE']
    quotes_paginated = quotes.query.paginate(page, per_page, False)
    speakers = people_quoted

    return render_template('quotes.html',
                            title = 'Quotes',
                            quotes_data = quotes_paginated.items,
                            speakers = speakers,
                            pagination = quotes_paginated)




if __name__=='__main__':
    app.run(debug=True)
