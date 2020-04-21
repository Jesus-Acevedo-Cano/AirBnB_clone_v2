#!/usr/bin/python3
# start a flask web app
from flask import Flask, render_template
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

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
