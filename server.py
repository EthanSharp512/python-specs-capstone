"""I Was There"""
import imp
from os import environ

from jinja2 import StrictUndefined
from flask import Flask, render_template, redirect, jsonify, render_template_string, request, flash, session, url_for, abort
from flask_debugtoolbar import DebugToolbarExtension
from flask_login import LoginManager, login_user, login_required, logout_user
from werkzeug.security import generate_password_hash, check_password_hash

from model import User, Genre, Subgenre, Event, Post, connect_to_db, db
from forms import AddEventForm, AddPostForm, LoginForm, RegistrationForm

login_manager = LoginManager()

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = environ['URI']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.secret_key = environ["SECRET_KEY"]

app.jinja_env.undefined = StrictUndefined


login_manager.init_app(app)
login_manager.login_view = 'login'














#app routes

#home
@app.route("/")
def home():
    return render_template("home.html")


@app.route('/welcome')
@login_required
def welcome_user():
    return render_template('welcome.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You have been logged out!")
    return redirect(url_for('home'))

@app.route('/login', methods=['GET', 'POST'])
def login():

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user.check_password(form.password.data) and user is not None:
            
            login_user(user)
            flash('Logged in successfully!')

            next = request.args.get('next')

            if next == None or not next[0]=='/':
                next = url_for('welcome')

            return redirect(next)

        return render_template('login.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        user = User(email=form.email.data, username=username.form.data,password=form.password.data)

        db.session.add(user)
        db.session.commit()
        flash("You have ben registered!")
        return redirect(url_for('login'))
    return render_template('register.html', form=form)



#see all public posts
@app.route('/feed')
def feed():
    events = Event.query.all()
    user = User.query.filter_by(user_id=Event.user_id).first()
    genre = Genre.query.filter_by(genre_id=Event.genre_id).first()
    return render_template('feed.html', events=events, user=user, genre=genre)


#user event form
@app.route('/new', methods=['GET', 'POST'])
def new_event():
        
    form = AddEventForm()

    form.populate_genre_field()

    genres = Genre.query.all()

    if form.validate_on_submit():

        event_name = form.event_name.data
        artist = form.artist.data
        location = form.location.data
        event_date = form.event_date.data
        public = form.public.data
        user_id = 1
        genre_id = form.genre_id.data
        
        new_event = Event(event_name, artist, location, event_date, public, user_id, genre_id)

        db.session.add(new_event)
        db.session.commit()

        return redirect(url_for('my_profile'))
    print('genres')
    return render_template('new_event_form.html', form=form, genres=genres)


#dependent dropdown subgenre
@app.route("/genre",methods=["POST","GET"])
def carbrand():  
    if request.method == 'POST':
        category_id = request.form['category_id']   
        subgenre = Subgenre.query.filter_by(genre_id=category_id)  
        OutputArray = []
        for row in subgenre:
            outputObj = {
                'id': row['genre_id'],
                'name': row['sub_genre']}
            OutputArray.append(outputObj)
    return jsonify(OutputArray)


#view public event detaials
@app.route('/event/<int:event_id>')
def event_details(event_id):
    """show event details and posts"""

    posts = Post.query.filter_by(event_id=event_id).all()
    event = Event.query.filter_by(event_id=event_id).first()
    user = User.query.filter_by(user_id=Event.user_id).first()
    genre = Genre.query.filter_by(genre_id=Event.genre_id).first()
    return render_template('view_event.html', event=event, user=user, genre=genre, posts=posts)


#view users events
@app.route('/profile')
def my_profile():

    events = Event.query.all()
    user = User.query.filter_by(user_id=Event.user_id).first()
    genre = Genre.query.filter_by(genre_id=Event.genre_id).first()
    return render_template('profile.html', events=events, user=user, genre=genre)


#view users event details
@app.route('/my_event/<int:event_id>')
def my_event(event_id):
    """show event details and posts"""

    event = Event.query.filter_by(event_id=event_id).first()
    user = User.query.filter_by(user_id=Event.user_id).first()
    genre = Genre.query.filter_by(genre_id=Event.genre_id).first()

    posts = Post.query.filter_by(event_id=event_id).all()
    return render_template('my_event.html', event=event, user=user, genre=genre, posts=posts)


#add post from users profile on specific event
@app.route('/add_post/<int:event_id>', methods=['GET', 'POST'])
def add_post(event_id):

    form = AddPostForm()

    if form.validate_on_submit():

        content_link = form.content_link.data
        post_caption = form.post_caption.data
        user_id = 1

        new_post = Post(event_id, content_link, post_caption, user_id)

        db.session.add(new_post)
        db.session.commit()

        return redirect(url_for('my_event', event_id=event_id))


    return render_template('add_post.html', form=form)


#delete post from users specific event
@app.route('/delete_post/<int:post_id>', methods=['GET', 'POST'])
def delete_post(post_id):

    event = Event.query.filter_by(event_id=Post.event_id).first()
    event_id = event.event_id
    deleted_post = Post.query.get(post_id)

    db.session.delete(deleted_post)
    db.session.commit()

    return redirect(url_for('my_event', event_id=event_id))

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