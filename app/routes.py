from flask import render_template, flash, redirect,  url_for,request
from flask_login import current_user, login_user, logout_user,login_required
from werkzeug.urls import url_parse
from app.forms import LoginForm, RegistrationForm
from app import app,db
from app.models import users


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
    return render_template('about.html')

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
        administrator verify before")
        return redirect(url_for('login'))
    return render_template('signup.html', title='signup', form=form)

if __name__=='__main__':
    app.run(debug=True)
