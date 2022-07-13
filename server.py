"""I Was There"""
from os import environ

from jinja2 import StrictUndefined

from flask import Flask, render_template, redirect, request, flash, session
from flask_debugtoolbar import DebugToolbarExtension

from model import User, Genre, Subgenre, Event, Post, connect_to_db, db

app = Flask(__name__)

app.secret_key = environ["SECRET_KEY"]

app.jinja_env.undefined = StrictUndefined

#app routes

@app.route("/")
def home():
    return render_template("home.html")







if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.env = 'development'
    # make sure templates, etc. are not cached in debug mode
    app.jinja_env.auto_reload = app.debug

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(port=5000, host='0.0.0.0', debug=True)