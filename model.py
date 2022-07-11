from enum import auto, unique
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
db = SQLAlchemy(app)


class User(db.Model):
    """User of I Was There website"""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    email = db.Column(db.String(64, unique=True))

class Event(db.Model):
    pass

class Post(db.Model):
    pass

class Genre(db.Model):
    pass

class Subgenre(db.Model):
    pass