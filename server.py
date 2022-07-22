from os import environ

from jinja2 import StrictUndefined
from flask import Flask, render_template, redirect, jsonify, request, flash, url_for
from flask_debugtoolbar import DebugToolbarExtension
from flask_login import LoginManager, login_user, login_required, logout_user, current_user

from model import User, Genre, Subgenre, Event, Post, connect_to_db, db
from forms import AddEventForm, AddPostForm, UpdateEventForm, LoginForm, RegistrationForm

app = Flask(__name__)

login_manager = LoginManager(app)

app.config['SQLALCHEMY_DATABASE_URI'] = environ['URI']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.secret_key = environ["SECRET_KEY"]

app.jinja_env.undefined = StrictUndefined

login_manager.init_app(app)
login_manager.login_view = 'login'

#app routes

#gets current user
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

#home page
@app.route("/")
def home():
    return render_template("home.html")

#logs out user
@app.route('/logout')
@login_required
def logout():

    logout_user()

    flash("You have been logged out!")
    return redirect(url_for('home'))

#logs in user
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
                next = url_for('home')

            return redirect(next)

    return render_template('login.html', form=form)

#registers user
@app.route('/register', methods=['GET', 'POST'])
def register():

    form = RegistrationForm()

    if form.validate_on_submit():

        user = User(email=form.email.data, username=form.username.data, password=form.password.data)

        db.session.add(user)
        db.session.commit()

        flash("You have been registered!")
        return redirect(url_for('login'))

    return render_template('register.html', form=form)

#see all public posts in feed
@app.route('/feed')
def feed():

    events = Event.query.all()
    user = User.query.filter_by(user_id=Event.user_id).first()
    genre = Genre.query.filter_by(genre_id=Event.genre_id).first()
    sub_genre = Subgenre.query.filter_by(sub_genre_id=Event.sub_genre_id).first()

    return render_template('feed.html', events=events, user=user, genre=genre, sub_genre=sub_genre)

#new user event form
@app.route('/new', methods=['GET', 'POST'])
@login_required
def new_event():
        
    form = AddEventForm()
    form.populate_genre_field()
    genres = Genre.query.all()

    if request.method == "POST":

        event_name = form.event_name.data
        artist = form.artist.data
        location = form.location.data
        event_date = form.event_date.data
        public = form.public.data
        user_id = current_user.user_id
        genre_id = form.genre_id.data
        sub_genre_id = form.sub_genre_id.data
        new_event = Event(event_name, artist, location, event_date, public, user_id, genre_id, sub_genre_id)

        db.session.add(new_event)
        db.session.commit()

        return redirect(url_for('my_profile'))

    return render_template('new_event_form.html', form=form, genres=genres)

#dependent dropdown for sub genres
@app.route("/subgenre",methods=["POST","GET"])
def dependent_genre():  

    if request.method == 'POST':

        category_id = request.form['category_id']   
        subgenre = Subgenre.query.filter(Subgenre.genre_id == category_id).all()
        OutputArray = []

        for row in subgenre:
            row = row.__dict__
            outputObj = {
                'id': row['sub_genre_id'],
                'name': row['sub_genre']}
            OutputArray.append(outputObj)

    return jsonify(OutputArray)

#updates event info
@app.route('/update_event/<int:event_id>', methods=['GET', 'POST'])
@login_required
def update_event(event_id):

    form = UpdateEventForm()
    form.populate_genre_field()
    updated = Event.query.get(event_id)
    event = Event.query.filter_by(event_id=event_id).first()

    if request.method == 'POST':
        updated.event_name = form.event_name.data
        updated.artist = form.artist.data
        updated.location = form.location.data
        updated.event_date = form.event_date.data
        updated.public = form.public.data
        updated.genre_id = form.genre_id.data
        updated.sub_genre_id = form.sub_genre_id.data

        db.session.commit()

        return redirect(url_for('my_event', event_id=event_id))

    return render_template('update_event.html', form=form, event=event)

#view public event details
@app.route('/event/<int:event_id>')
def event_details(event_id):

    posts = Post.query.filter_by(event_id=event_id).all()
    event = Event.query.filter_by(event_id=event_id).first()
    user = User.query.filter_by(user_id=Event.user_id).first()
    genre = Genre.query.filter_by(genre_id=Event.genre_id).first()
    sub_genre = Subgenre.query.filter_by(sub_genre_id=Event.sub_genre_id).first()

    return render_template('view_event.html', event=event, user=user, genre=genre, posts=posts, sub_genre=sub_genre)

#view current users events
@app.route('/profile')
@login_required
def my_profile():

    events = Event.query.filter_by(user_id=current_user.user_id).all()
    user = User.query.filter_by(user_id=current_user.user_id).first()
    genre = Genre.query.filter_by(genre_id=Event.genre_id).first()
    sub_genre = Subgenre.query.filter_by(sub_genre_id=Event.sub_genre_id).first()

    return render_template('profile.html', events=events, user=user, genre=genre, sub_genre=sub_genre)

#view current users event details
@app.route('/my_event/<int:event_id>')
@login_required
def my_event(event_id):

    event = Event.query.filter_by(event_id=event_id).first()
    user = User.query.filter_by(user_id=Event.user_id).first()
    genre = Genre.query.filter_by(genre_id=Event.genre_id).first()
    sub_genre = Subgenre.query.filter_by(sub_genre_id=Event.sub_genre_id).first()
    posts = Post.query.filter_by(event_id=event_id).all()

    return render_template('my_event.html', event=event, user=user, genre=genre, posts=posts, sub_genre=sub_genre)

#add post from current users profile on specific event
@app.route('/add_post/<int:event_id>', methods=['GET', 'POST'])
@login_required
def add_post(event_id):

    form = AddPostForm()

    if form.validate_on_submit():

        content_link = form.content_link.data
        post_caption = form.post_caption.data
        user_id = current_user.user_id
        new_post = Post(event_id, content_link, post_caption, user_id)

        db.session.add(new_post)
        db.session.commit()

        return redirect(url_for('my_event', event_id=event_id))

    return render_template('add_post.html', form=form)

#create a post on a public event, current users event or other users event
@app.route('/public_post/<int:event_id>', methods=['GET', 'POST'])
@login_required
def public_post(event_id):

    form = AddPostForm()

    if form.validate_on_submit():

        content_link = form.content_link.data
        post_caption = form.post_caption.data
        user_id = current_user.user_id
        new_post = Post(event_id, content_link, post_caption, user_id)

        db.session.add(new_post)
        db.session.commit()

        return redirect(url_for('event_details', event_id=event_id))

    return render_template('add_post.html', form=form)

#delete entire event from current users profile
@app.route('/delete_event/<int:event_id>', methods=['GET', 'POST'])
@login_required
def delete_event(event_id):

    user = User.query.filter_by(user_id=Event.user_id).first()
    user_id = user.user_id
    deleted_event = Event.query.get(event_id)

    db.session.delete(deleted_event)
    db.session.commit()

    return redirect(url_for('my_profile', user_id=user_id))

#delete post from current users specific event
@app.route('/delete_post/<int:post_id>/<int:event_id>', methods=['GET', 'POST'])
@login_required
def delete_post(post_id, event_id):

    event = Event.query.filter_by(event_id=Post.event_id).first()
    deleted_post = Post.query.get(post_id)

    db.session.delete(deleted_post)
    db.session.commit()

    return redirect(url_for('my_event', event_id=event_id))

#delete a post from a public event from the feed
@app.route('/delete_pubpost/<int:post_id>/<int:event_id>', methods=['GET', 'POST'])
@login_required
def delete_pubpost(post_id, event_id):

    event = Event.query.filter_by(event_id=Post.event_id).first()
    deleted_post = Post.query.get(post_id)

    db.session.delete(deleted_post)
    db.session.commit()

    return redirect(url_for('event_details', event_id=event_id))


if __name__ == "__main__":

    app.env = 'development'
    app.jinja_env.auto_reload = app.debug

    connect_to_db(app)
    DebugToolbarExtension(app)

    app.run(port=5000, host='0.0.0.0', debug=True)