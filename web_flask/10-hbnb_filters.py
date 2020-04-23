#!/usr/bin/python3
# start a flask web app
from flask import Flask, render_template
from models import storage
app = Flask(__name__)


@app.route('/', strict_slashes=False)
def hello_hbnb():
    """print Hello HBNB!"""
    return "Hello HBNB!"


@app.route('/hbnb', strict_slashes=False)
def hbnb():
    """print HBNB"""
    return "HBNB"


@app.route('/c/<text>', strict_slashes=False)
def c_text(text):
    """print c <text>"""
    return "C {}".format(text.replace("_", " "))


@app.route('/python', strict_slashes=False)
@app.route('/python/<text>', strict_slashes=False)
def python_text(text="is cool"):
    """print python <text>"""
    return "Python {}".format(text.replace("_", " "))


@app.route('/number/<int:n>', strict_slashes=False)
def number_n(n):
    """print only number <n>"""
    return "{} is a number".format(n)


@app.route('/number_template/<int:n>', strict_slashes=False)
def number_template(n):
    """print template only if  number <n>"""
    return render_template('5-number.html', var=n)


@app.route('/number_odd_or_even/<int:n>', strict_slashes=False)
def number_odd_or_even(n):
    """print template if number <n> odd or even"""
    if n % 2 == 0:
        var = "{} is even".format(n)
    else:
        var = "{} is odd".format(n)
    return render_template('6-number_odd_or_even.html', var=var)


@app.teardown_appcontext
def teardown_(exc):
    """close session"""
    storage.close()


@app.route('/states_list', strict_slashes=False)
def states_list():
    """print template only if  states_list"""
    var = storage.all("State")
    return render_template('7-states_list.html', var=var)


@app.route('/cities_by_states', strict_slashes=False)
def cities_by_states():
    """print template only if  states_list"""
    var = []
    var.append(storage.all("State"))
    var.append(storage.all("City"))
    return render_template('8-cities_by_states.html', var=var)


@app.route('/states', strict_slashes=False)
@app.route('/states/<id>', strict_slashes=False)
def states(id=None):
    var = []
    if id is not None:
        for state in storage.all("State").values():
            if state.id == id:
                var.append({"State": state})
                var.append(storage.all("City"))
                return render_template("9-states.html", var=var)
        return render_template('9-states.html', var=None)
    var.append(storage.all("State"))
    return render_template('9-states.html', var=var)


@app.route('/hbnb_filters', strict_slashes=False)
def hbnb_filters():
    """filters template"""
    var = []
    var.append(storage.all("State"))
    var.append(storage.all("City"))
    var.append(storage.all("Amenity"))
    return render_template('10-hbnb_filters.html', var=var)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
