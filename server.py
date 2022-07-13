"""I Was There"""
from os import environ

from jinja2 import StrictUndefined
from flask import Flask, render_template, redirect, request, flash, session, url_for
from flask_debugtoolbar import DebugToolbarExtension

from model import User, Genre, Subgenre, Event, Post, connect_to_db, db
from forms import AddEventForm

app = Flask(__name__)

app.secret_key = environ["SECRET_KEY"]

app.jinja_env.undefined = StrictUndefined

#app routes

@app.route("/")
def home():
    return render_template("home.html")

@app.route('/new', methods=['GET', 'POST'])
def new_event():
        
    form = AddEventForm()

    if form.validate_on_submit():

        event_name = form.event_name.data
        artist = form.artist.data
        location = form.location.data
        event_date = form.event_date.data
        public = form.public.data
        genre = form.genre.data
        subgenre = form.subgenre.data
        
        new_event = Event(event_name, artist, location, event_date, public, genre, subgenre)

        db.session.add(new_event)
        db.session.commit()

        return redirect(url_for('profile'))

    return render_template('new_event_form.html', form=form)

@app.route('/profile')
def my_profile():

    events = Event.query.all()
    return render_template('profile.html', events=events)


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