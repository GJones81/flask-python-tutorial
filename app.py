from flask import Flask, render_template, jsonify, request, redirect
from flask_nav import Nav
from flask_nav.elements import Navbar,View
from pymongo import MongoClient

app = Flask(__name__)
nav = Nav(app)
app.config['DEBUG'] = True

client = MongoClient()
db = client.python_flask_pymongo
collection = db.operators

nav.register_element('my_navbar', Navbar('the_nav',
        View('Home Page', 'home_page'), 
        View('Loops Page', 'loops_page'),
        View('Operators Page', 'operators_page')))

@app.route('/')
def home_page():
    return render_template('index.html')

@app.route('/loops')
def loops_page():
    return render_template('loops.html')

@app.route('/operators', methods = ['GET', 'POST'])
def operators_page():
    if request.method == 'POST':
        collection.insert_one({
            'name': request.form['name'],
            'description': request.form['description'],
            'symbol': request.form['symbol'],
            'example': request.form['example'],
            'uses': request.form['uses']
        })
        return redirect('/operators')
    else:
        operators = collection.find()
        return render_template('operators.html', operators = operators)

if __name__ == '__main__':
    app.run()
