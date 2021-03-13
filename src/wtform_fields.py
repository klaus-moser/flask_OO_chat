from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, EqualTo, ValidationError

from models.user import UserModel


class RegistrationForm(FlaskForm):
    """
    This is the form class for the Registration.
    """
    username = StringField('username_label', validators=[
        InputRequired(message='Username required!'),
        Length(min=4, max=25, message='Username must be between 4-25 characters!')])

    password = PasswordField('password_label', validators=[
        InputRequired(message='Password required!'),
        Length(min=4, max=25, message='Password must be between 4-25 characters!')])

    confirm_pswd = PasswordField('confirm_pswd_label', validators=[
        InputRequired(message='Password required!'),
        EqualTo('password', message='Passwords must match!')])

    submit_button = SubmitField('Create')

    # Custom validator to check username upfront
    def validate_username(self, username) -> None:
        """
        Validate a given username.
        :param username: Username to be validated via the database.
        :return: None.
        """
        if UserModel.find_by_username(username=username.data):
            raise ValidationError("A user '{}' already exists!".format(username.data))


class LoginForm(FlaskForm):
    """
    This is the form class for the Registration.
    """
    username = StringField('username_label', validators=[
        InputRequired(message='Username required!')])

    password = PasswordField('password_label', validators=[
        InputRequired(message='Password required!')])  # , invalid_credentials])

    submit_button = SubmitField('Login')

    # Custom validator to check username during login
    def validate_username(self, username_entered: StringField) -> None:

        # Search database for given user
        user = UserModel.find_by_username(username=username_entered.data)

        # Check if username is valid (exists)
        if user is None:
            raise ValidationError("Username is incorrect!")

    # Custom validator to check password during login
    def validate_password(self, password_entered: PasswordField) -> None:

        # Search database for given user
        user = UserModel.find_by_username(username=self.username.data)

        # Check if password is valid
        if user is not None:
            if password_entered.data != user.password:
                raise ValidationError("Password is incorrect!")
