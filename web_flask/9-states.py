#!/usr/bin/python3
"""script that starts a Flask web application"""
from models import storage
from flask import Flask, render_template
from models.state import State
from models.city import City

app = Flask(__name__)


@app.route('/states', strict_slashes=False)
def display_states():
    """Display all states"""
    states = storage.all(State)
    states_list = sorted(states.values(), key=lambda x: x.name)
    return render_template('9-states.html', states=states_list)


@app.route('/states/<id>', strict_slashes=False)
def display_state_cities(id):
    """display Cities in State object if id found"""
    states = storage.all(State)
    state_cities = []
    for state in states.values():
        if state.id == id:
            state_cities = sorted(state.cities, key=lambda x: x.name)
            break
    if state_cities:
        return render_template('9-states.html', state=state, cities=state_cities)
    else:
        return render_template('9-states.html', not_found=True)


@app.teardown_appcontext
def teardown(exception):
    """close section"""
    storage.close()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
