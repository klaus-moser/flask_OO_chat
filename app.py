from flask import Flask, render_template
from os import environ

from src.wtform_fields import RegistrationForm
from src.db import db


# Configure app
app = Flask(__name__)
app.secret_key = ']K~B;aF>5/`/]h3xoZ8'

# Configure database
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DATABASE_URL', 'sqlite:///data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)


# Create database before first request
@app.before_first_request
def create_tables() -> None:
    """
    Creates all the tables (it sees) in a data.db file,
    before the first request.
    """
    db.create_all()


# Endpoint
@app.route('/', methods=['GET', 'POST'])
def index():
    """
    Index.
    """
    reg_form = RegistrationForm()

    if reg_form.validate_on_submit():  # True if all validation rules are cleared
        return "Great success!"

    return render_template('index.html', form=reg_form)


if __name__ == "__main__":
    app.run(debug=True, host='127.0.0.1', port=5000)
