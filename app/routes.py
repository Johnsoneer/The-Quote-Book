from flask import render_template, flash, redirect,  url_for,request
from flask_login import current_user, login_user, logout_user,login_required
from werkzeug.urls import url_parse
from app.forms import LoginForm, RegistrationForm, VerifyUserForm
from app import app,db
from app.models import users
from app.data_objects import VerificationTable



'''
This is the main script for executing the flask functions so we can
send our html templates to the browser for rendering. We boot, handle requests,
and configure our server right here.

Read more about Flask how-to here:
https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world
'''


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

@app.route('/admin/<username>', methods=['GET','POST'])
@login_required
def admin(username):
    user = users.query.filter_by(username=username).first_or_404()
    is_admin = user.is_admin
    if is_admin ==False:
        flash("You are not an administrator. Quit trying to access the \
        admin panel!")
        return redirect(url_for('home'))

    user_data_raw = users.query.all()
    user_data = VerificationTable(user_data_raw,user)

    data = {'current_user':current_user,
            'table':user_data_raw}
    return render_template('admin.html',title = 'Administrator Panel',data = data)

@app.route('/verify_user/<username>/<verify_username>', methods=['GET','POST'])
@login_required
def verify_user(username,verify_username):
    user = users.query.filter_by(username=username).first_or_404()
    is_admin = user.is_admin
    if is_admin ==False:
        flash("You are not an administrator. Quit trying to access the \
        admin panel!")
        return redirect(url_for('home'))

    user_to_verify = users.query.filter_by(username=verify_username).first()
    user_to_verify.is_verified = True
    db.session.add(user_to_verify)
    db.session.commit()

    return redirect(url_for('/admin/{}'.format(user.username)))


if __name__=='__main__':
    app.run(debug=True)
