#!/usr/bin/python3
"""script that starts a Flask web application"""
from models import storage
from flask import Flask, render_template
from models.state import State

app = Flask(__name__)


@app.route('/cities_by_states', strict_slashes=False)
def display_states():
    """routes cities by state into html fIle"""
    states = storage.all(State)
    states_list = sorted(states.values(), key=lambda x: x.name)
    return render_template('8-cities_by_states.html', states=states_list)


@app.teardown_appcontext
def teardown(exception):
    """close session"""
    storage.close()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
