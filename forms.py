from xmlrpc.client import Boolean
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, DateField, BooleanField, SelectField

class AddEventForm(FlaskForm):

    event_name = StringField('Name of event: ')
    artist = StringField('Name of artist: ')
    location = StringField('Location of event: ')
    event_date = DateField('Date of event: ')
    public = BooleanField('Make event private: ')
    genre = SelectField('Select a genre: ')
    subgenre = SelectField('Select sub-genre if applicable: ')
    submit = SubmitField('Create Event')
