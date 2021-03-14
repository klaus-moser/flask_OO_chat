from flask import Flask, render_template, redirect, url_for
from flask_login import LoginManager, login_user, current_user, login_required, logout_user
from passlib.hash import pbkdf2_sha256
from os import environ

from src.wtform_fields import RegistrationForm, LoginForm
from models.user import UserModel
from src.db import db

# Configure app
app = Flask(__name__)
app.secret_key = ']K~B;aF>5/`/]h3xoZ8'

# Configure database
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DATABASE_URL', 'sqlite:///data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# Configure flask login
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return UserModel.find_by_id(id_=user_id)


# Create database before first request
@app.before_first_request
def create_tables() -> None:
    """
    Creates all the tables (it sees) in a data.db file,
    before the first request.
    """
    db.create_all()


# Endpoints
@app.route('/', methods=['GET', 'POST'])
def index():
    """
    Index.
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
        return redirect(url_for('login'))

    # Return the index page [GET]
    return render_template('index.html', form=reg_form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    Login.
    """
    login_form = LoginForm()

    # Allow login if validation succeeded [POST]
    if login_form.validate_on_submit():

        # Login user
        user = UserModel.find_by_username(username=login_form.username.data)
        login_user(user=user)

        # Check if user is logged in
        if current_user.is_authenticated:
            return "Logged in!"
        return "NOT logged in ..."

    # Return login page [GET]
    return render_template("login.html", form=login_form)


@app.route('/chat', methods=['GET', 'POST'])
@login_required  # flask-login: Decorator to check if/that user is logged in
def chat():


    return "Lets chat!"


@app.route('/logout', methods=['GET'])
@login_required  # flask-login: Decorator to check if/that user is logged in
def logout():

    # Logout user
    logout_user()
    return "Logged out!"


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
