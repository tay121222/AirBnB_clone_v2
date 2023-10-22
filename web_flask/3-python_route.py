#!/usr/bin/python3
"""script that starts a Flask web application"""
from flask import Flask

app = Flask(__name__)


@app.route('/', strict_slashes=False)
def hello_hbnb():
    """Route index"""
    return 'Hello HBNB!'


@app.route('/hbnb', strict_slashes=False)
def show_hbnb():
    """Route to hbnb"""
    return 'HBNB'


@app.route('/c/<text>', strict_slashes=False)
def display_c(text="is cool"):
    """Routes"""
    return 'C {}'.format(text.replace('_', ' '))


@app.route('/python/', strict_slashes=False)
@app.route('/python/<text>', strict_slashes=False)
def display_python(text='is_cool'):
    """More Routes"""
    return 'Python {}'.format(text.replace('_', ' '))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
