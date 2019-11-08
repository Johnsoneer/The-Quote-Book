from flask import render_template, flash, redirect,  url_for
from app.forms import LoginForm
from app import app


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
def about():
    return render_template('about.html')

@app.route('/login/',methods=['GET',"POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data))
        return redirect(url_for('home'))
    return render_template('login.html',title='Sign In', form=form)

if __name__=='__main__':
    app.run(debug=True)
