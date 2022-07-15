from xmlrpc.client import Boolean
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, DateField, BooleanField, SelectField, TextAreaField

from model import Genre

class AddEventForm(FlaskForm):

    event_name = StringField('Name of event: ')
    artist = StringField('Name of artist: ')
    location = StringField('Location of event: ')
    event_date = DateField('Date of event: ')
    public = BooleanField('Make event public: ')
    genre_id = SelectField('Select a genre: ')
    submit = SubmitField('Create Event')


    def populate_genre_field(self):

        genres = Genre.query.all()
        genreList = [(i.genre_id, i.genre) for i in genres]
        self.genre_id.choices=genreList

class AddPostForm(FlaskForm):

    content_link = TextAreaField("Paste a link to a video or image taken at the event: ")
    post_caption = TextAreaField("Write a caption for the linked content: ")
    submit = SubmitField('Post')

