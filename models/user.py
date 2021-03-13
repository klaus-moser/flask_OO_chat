from src.db import db


class UserModel(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25), unique=True, nullable=False)
    password = db.Column(db.String(25), nullable=False)

    def __init__(self, username=None, password=None):
        self.username = username
        self.password = password

    @classmethod
    def find_by_username(cls, username: str) -> object:
        """
        Find an user by the given username.
        :param username: Username to search for the user.
        :return: Object of the User class.
        """
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_id(cls, id_: str) -> object:
        """
        Find a user by the given id.
        :param id_: ID to search for the user.
        :return: Object of the User class.
        """
        return cls.query.filter_by(id=id_).first()

    def save_to_db(self) -> None:
        """
        Save to data base.
        """
        db.session.add(self)
        db.session.commit()
