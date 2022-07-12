from os import environ

from enum import auto, unique
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey


db = SQLAlchemy()


class User(db.Model):
    """User of I Was There website"""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    username = db.Column(db.String(64), unique=True)
    email = db.Column(db.String(255, unique=True))
    password = db.Column(db.String(64))
    first_name = db.Column(db.String(64))
    last_name = db.Column(db.String(64))

    def __repr__(self):
        return f"""<User user_id={self.user_id} 
                   username={self.username} 
                   email={self.email} 
                   password={self.password}
                   first_name={self.first_name} 
                   last_name={self.last_name}>"""


class Genre(db.Model):
    """"Genre of I Was There website"""

    __tablename__ = "genres"

    genre_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    genre = db.Column(db.String(64))

    def __repr__(self):
        return f"""<Genre genre_id={self.genre_id} 
                   genre={self.genre}>"""


class Subgenre(db.Model):
    """Subgenre of I Was There website"""

    __tablename__ = "subgenres"

    sub_genre_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    sub_genre = db.Column(db.String(64))
    genre_id = db.Column(db.Integer, db.ForeignKey('genres.genre_id'))

    #Relationship to genres table
    genre = db.relationship("Genre", backref=db.backref("subgenres", order_by=sub_genre_id))

    def __repr__(self):
        return f"""<Subgenre sub_genre_id={self.sub_genre_id} 
                   sub_genre={self.sub_genre} 
                   genre_id={self.genre_id}>"""


class Event(db.Model):
    """Event of I Was There website"""

    __tablename__ = "events"

    event_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    event_name = db.Column(db.String(128))
    artist = db.Column(db.String(64))
    location = db.Column(db.String(255))
    # date = db.Column(db.datetime.date)
    # public = db.Column(db.Boolean)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    genre_id = db.Column(db.Integer, db,ForeignKey('genres.genre_id'))
    sub_genre_id = db.Column(db.Integer, db,ForeignKey('subgenres.sub_genre_id'))

    #Relationships to users, genres, and subgenres tables
    user = db.relationship("User", backref=db.backref("events", order_by=event_id))
    genre = db.relationship("Genre", backref=db.backref("events", order_by=event_id))
    sub_genre = db.relationship("Subgenre", backref=db.backref("events", order_by=event_id))

    def __repr__(self):
        return f"""<Event event_id={self.event_id} 
                   event_name={self.event_name} 
                   artist={self.artist} 
                   location={self.location}
                   date={self.date} 
                   public={self.public}
                   user_id={self.user_id}
                   genre_id={self.genre_id}
                   sub_genre_id{self.sub_genre_id}>"""


class Post(db.Model):
    """Post of I Was There website"""

    __tablename__ = "posts"

    post_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('events.event_id'))
    content_link = db.Column(db.String(500))
    post_caption = db.Column(db.String(255))
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))

    #Relationships to events and users tables
    event = db.relationship("Event", backref=db.backref("events", order_by=post_id))
    user = db.relationship("User", backref=db.backref("posts", order_by=post_id))

    def __repr__(self):
        return f"""<Post post_id={self.post_id} 
                   event_id={self.event_id} 
                   content_link={self.content_link} 
                   post_caption={self.post_caption}
                   user_id={self.user_id}>"""


def connect_to_db(app):
    """Connect the database to Flask app."""

    app.config['SQLALCHEMY_DATABASE_URI'] = environ['URI']
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)


if __name__ == "__main__":

    from server import app
    connect_to_db(app)
    print("Connected to DB.")