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

    def validate_credentials(self, field: PasswordField) -> None:
        """
        Check the credentials from the LoginForm.
        :return: None.
        """
        username_entered = self.username.data
        password_entered = field.data

        user = UserModel.find_by_username(username=username_entered)

        # Check if credentials are valid
        if user is None:
            raise ValidationError("Username or password is incorrect!")
        elif password_entered != user.password:
            raise ValidationError("Username or password is incorrect!")

    username = StringField('username_label', validators=[
        InputRequired(message='Username required!')])

    password = PasswordField('password_label', validators=[
        InputRequired(message='Password required!'), validate_credentials])

    submit_button = SubmitField('Login')
