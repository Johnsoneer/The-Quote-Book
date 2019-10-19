from flask import Flask, render_template, jsonify
from contrib.fetch import query_with_retry


app = Flask(__name__)


@app.route('/')

def home():
    return render_template('home.html')


@app.route('/about/')
def about():
    return render_template('about.html')

if __name__=='__main__':
    app.run(debug=True)
