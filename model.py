from os import environ

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

db = SQLAlchemy()

class User(db.Model, UserMixin):
    """User of I Was There website"""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    email = db.Column(db.String(255), unique=True)
    password_hash = db.Column(db.String(255))

    def __init__(self, email, username, password):
        self.email = email
        self.username = username
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_id(self):
           return (self.user_id)

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

    genre_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    genre = db.Column(db.String(64))

    def __init__(self, genre):
        self.genre = genre

    def __repr__(self):
        return f"""<Genre genre_id={self.genre_id} 
                   genre={self.genre}>"""


class Subgenre(db.Model):
    """Subgenre of I Was There website"""

    __tablename__ = "subgenres"

    sub_genre_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    genre_id = db.Column(db.Integer, db.ForeignKey('genres.genre_id'))
    sub_genre = db.Column(db.String(64))

    #Relationship to genres table
    genre = db.relationship("Genre", backref=db.backref("subgenres", order_by=sub_genre_id))

    def __init__(self, genre_id, sub_genre):
        self.genre_id = genre_id
        self.sub_genre = sub_genre

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
    event_date = db.Column(db.DateTime)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    public = db.Column(db.Boolean)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    genre_id = db.Column(db.Integer, db.ForeignKey('genres.genre_id'))
    sub_genre_id = db.Column(db.Integer, db.ForeignKey('subgenres.sub_genre_id'), nullable=True)

    #Relationships to users, genres, and subgenres tables
    user = db.relationship("User", backref=db.backref("events", order_by=event_id))
    genre = db.relationship("Genre", backref=db.backref("events", order_by=event_id))
    sub_genre = db.relationship("Subgenre", backref=db.backref("events", order_by=event_id))

    def __init__(self, event_name, artist, location, event_date, public, user_id, genre_id, sub_genre_id):
        self.event_name = event_name
        self.artist = artist
        self.location = location
        self.event_date = event_date
        self.public = public
        self.user_id = user_id
        self.genre_id = genre_id
        self.sub_genre_id = sub_genre_id

    def __repr__(self):
        return f"""<Event event_id={self.event_id} 
                   event_name={self.event_name} 
                   artist={self.artist} 
                   location={self.location}
                   event_date={self.event_date} 
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

    def __init__(self, event_id, content_link, post_caption, user_id):
        self.event_id = event_id
        self.content_link = content_link
        self.post_caption = post_caption
        self.user_id = user_id

    def __repr__(self):
        return f"""<Post post_id={self.post_id} 
                   event_id={self.event_id} 
                   content_link={self.content_link} 
                   post_caption={self.post_caption}
                   user_id={self.user_id}>"""


def connect_to_db(app):
    """Connect the database to Flask app."""

    db.app = app
    db.init_app(app)


if __name__ == "__main__":

    app = Flask(__name__)
    # app.config['SQLALCHEMY_DATABASE_URI'] = environ['URI']
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://xjnfkdqcajhlti:8c50b770fb757be4c76c35b5f7eb65cfec6a1e291183ca90ef59df4b243f0e58@ec2-52-207-15-147.compute-1.amazonaws.com:5432/d570t13ujc72v3'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    connect_to_db(app)
    print("Connected to DB.")