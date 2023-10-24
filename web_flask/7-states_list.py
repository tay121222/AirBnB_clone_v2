#!/usr/bin/python3
"""script that starts a Flask web application"""
from models import storage
from flask import Flask, render_template
from models.state import State

app = Flask(__name__)


@app.route('/states_list', strict_slashes=False)
def states_list():
    """display a HTML page"""
    states = storage.all(State)
    states_list = sorted(states.values(), key=lambda x: x.name)
    return render_template('7-states_list.html', states=states_list)


@app.teardown_appcontext
def teardown(exception):
    """Close Session"""
    storage.close()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
