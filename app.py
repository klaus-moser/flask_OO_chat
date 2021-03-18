from flask import Flask, render_template, redirect, url_for, flash
from flask_login import LoginManager, login_user, current_user, logout_user
from flask_socketio import SocketIO, send
from passlib.hash import pbkdf2_sha256
from time import localtime, strftime
from os import environ

from src.wtform_fields import RegistrationForm, LoginForm
from src.models.user import UserModel
from src.db import db


# Configure app
app = Flask(__name__)
app.secret_key = ']K~B;aF>5/`/]h3xoZ8'

# Configure database
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DATABASE_URL', 'sqlite:///data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app=app)

# Initialize Flask-SocketIO
socketio = SocketIO(app=app, logger=False, engineio_logger=False)


@app.before_first_request
def create_tables() -> None:
    """
    Creates all the tables (it sees) in a data.db file,
    before the first request.
    """
    db.create_all()


# Configure flask-login
login_manager = LoginManager()
login_manager.init_app(app=app)


@login_manager.user_loader
def load_user(user_id: str) -> object:
    """
    Load a user when he logs in an give it to the login_manager.
    :param user_id: Userid.
    :return: User object.
    """
    return UserModel.find_by_id(id_=user_id)


# Endpoints
@app.route('/', methods=['GET', 'POST'])
def index():
    """
    Index page.
    """
    reg_form = RegistrationForm()

    # Update database if validation succeeded [POST]
    if reg_form.validate_on_submit():
        username = reg_form.username.data
        password = reg_form.password.data

        # Hashing: incl. 16-byte salt (auto) + 29.000 iterations (default)
        hashed_password = pbkdf2_sha256.hash(password)

        # Save user to database
        user = UserModel(username=username, password=hashed_password)
        user.save_to_db()

        # Flash message
        flash("Registered successfully. Please login!", 'success')  # Opt. cat. parameter
        return redirect(url_for('login'))

    # Return the index page [GET]
    return render_template('index.html', form=reg_form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    Login page.
    """
    login_form = LoginForm()

    # Allow login if validation succeeded [POST]
    if login_form.validate_on_submit():
        # Login user
        user = UserModel.find_by_username(username=login_form.username.data)
        login_user(user=user)

        # Redirect to chat, then check there if user is logged in
        return redirect(url_for('chat'))

    # Return login page [GET]
    return render_template('login.html', form=login_form)


@app.route('/chat', methods=['GET', 'POST'])
def chat() -> str:
    """
    Chat page.
    :return: Message.
    """
    # TODO: Uncomment lines after testing
    """
    if not current_user.is_authenticated:

        # Flash message
        flash("Please login before accessing the chat!", 'danger')
        return redirect(url_for('login'))
    """
    return render_template('chat.html', username=current_user.username)


@app.route('/logout', methods=['GET'])
def logout() -> str:
    """
    Logout page.
    :return: Message.
    """
    # Logout user
    logout_user()

    # Flash message
    flash("You've been logged out!", 'success')
    return redirect(url_for('login'))


# Event handlers
@socketio.on('message')
def message(data):
    # TODO: add function description
    # It will send a message to the connected client(s)
    # pushes to the default/predefined event-bucket 'message'
    print("{}".format(data))
    send({'msg': data['msg'],
          'username': data['username'],
          # TODO: Is there a better timestamp format?
          'time_stamp': strftime('%b-%d %I:%M%p', localtime())})


if __name__ == "__main__":
    socketio.run(debug=True, host='0.0.0.0', port=5000, app=app)
