from ast import Pass
from flask import Flask
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, DateField, BooleanField, SelectField, TextAreaField, PasswordField, ValidationError
from wtforms.validators import DataRequired, Email, EqualTo

from model import Genre, User

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


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(),Email()])
    password = PasswordField('Password',validators=[DataRequired()])
    submit = SubmitField('Log In')
    

class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(),Email()])
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(),EqualTo('pass_confirm', message='Passwords must match!')])
    pass_confirm = PasswordField('Confirm Password', validators=[DataRequired()])
    submit = SubmitField('Register!')

    def check_email(self, email):
        if User.query.filter_by(email=self.email.data).first():
            raise ValidationError('That email has already been registered!')

    def check_username(self, username):
        if User.query.filter_by(email=self.username.data).first():
            raise ValidationError('That username has already been registered!')