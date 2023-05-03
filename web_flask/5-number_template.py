#!/usr/bin/python3
"""Starts a web application on 0.0.0.0:5000 with multiple routes"""

from flask import Flask, render_template

app = Flask(__name__)


@app.route('/', strict_slashes=False)
def hello():
    """Returns a page"""
    return "Hello HBNB!"


@app.route('/hbnb', strict_slashes=False)
def hbnb():
    """Returns a page"""
    return "HBNB"


@app.route('/c/<text>', strict_slashes=False)
def aboutC(text):
    """Returns a page based on parameter"""
    text = text.replace("_", " ")
    return "C {}".format(text)


@app.route('/python', strict_slashes=False)
@app.route('/python/<text>', strict_slashes=False)
def aboutPython(text="is cool"):
    text = text.replace('_', ' ')
    return "Python {}".format(text)


@app.route('/number/<int:n>', strict_slashes=False)
def numberInit(n):
    """Returns a page only if param is an integer"""
    if type(n) == int:
        return "{} is a number".format(n)


@app.route('/number_template/<int:n>', strict_slashes=False)
def templateNumberInit(n):
    """Returns a html page if n is am integer"""
    return render_template('5-number.html', n=n)


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
