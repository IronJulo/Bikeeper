from .app import db, session, login_manager
from typing import List
from flask_login import UserMixin

"""
Define model class
"""


class CONTACT(db.Model):
    id_contact = db.Column(db.Integer, primary_key=True)
    num_contact = db.Column(db.String(15))
    firstname_contact = db.Column(db.String(42))
    lastname_contact = db.Column(db.String(42))
    profile_picture_contact = db.Column(db.String(42))
    num_device = db.Column(db.String(15), db.ForeignKey("DEVICE.num_device"))
    DEVICE = db.relationship("DEVICE", backref=db.backref("CONTACT", lazy="dynamic"))


class LOG(db.Model):
    id_log = db.Column(db.Integer, primary_key=True)
    content_log = db.Column(db.String(150))
    type_log = db.Column(db.String(20))
    datetime_log = db.Column(db.DateTime())
    exception_log = db.Column(db.String(160))
    num_device = db.Column(db.String(15), db.ForeignKey("DEVICE.num_device"))
    DEVICE = db.relationship("DEVICE", backref=db.backref("LOG", lazy="dynamic"))


class DEVICE(db.Model):
    num_device = db.Column(db.String(15), primary_key=True)
    name_device = db.Column(db.String(42))
    row_parameters_device = db.Column(db.String(200))
    username_user = db.Column(db.String(42), db.ForeignKey("USER.username_user"))
    USER = db.relationship("USER", backref=db.backref("DEVICE", lazy="dynamic"))


class USER(db.Model, UserMixin):
    username_user = db.Column(db.String(42), primary_key=True)
    password_user = db.Column(db.String(200))
    num_user = db.Column(db.String(15))
    firstname_user = db.Column(db.String(42))
    lastname_user = db.Column(db.String(42))
    email_user = db.Column(db.String(80))
    town_user = db.Column(db.String(42))
    postal_code_user = db.Column(db.String(10))
    street_user = db.Column(db.String(95))
    profile_picture_user = db.Column(db.String(100))
    is_admin_user = db.Column(db.Boolean)

    def __init__(self, username, password, num, firstname, lastname, email, town,
                 postal_code, street, profile_picture, is_admin):
        self.username_user = username
        self.password_user = password
        self.num_user = num
        self.firstname_user = firstname
        self.lastname_user = lastname
        self.email_user = email
        self.town_user = town
        self.postal_code_user = postal_code
        self.street_user = street
        self.profile_picture_user = profile_picture
        self.is_admin_user = is_admin

    def get_id(self):
        return self.username_user


class MESSAGE(db.Model):
    id_message = db.Column(db.Integer, primary_key=True)
    is_admin_message = db.Column(db.Integer)
    datetime_message = db.Column(db.DateTime())
    content_message = db.Column(db.String(1000))
    id_ticket = db.Column(db.Integer, db.ForeignKey("TICKET.id_ticket"))
    TICKET = db.relationship("TICKET", backref=db.backref("MESSAGE", lazy="dynamic"))


class TICKET(db.Model):
    id_ticket = db.Column(db.Integer, primary_key=True)
    title_ticket = db.Column(db.String(100))
    is_closed_ticket = db.Column(db.Integer)
    username_user = db.Column(db.String(42), db.ForeignKey("USER.username_user"))
    USER = db.relationship("USER", backref=db.backref("TICKET", lazy="dynamic"))


class ORM:
    @staticmethod
    @login_manager.user_loader
    def load_user(username):
        return USER.query.filter(USER.username_user == username).first()

    @staticmethod
    def get_users():
        return USER.query.all()

    @staticmethod
    def get_user(pseudo: str) -> USER:
        """
        :param pseudo: user's nickname
        :return: USER: user instance
        """
        user = session.query(USER).get(pseudo)
        session.commit()
        return user

    @staticmethod
    def get_user_tickets(pseudo: str) -> List[TICKET]:
        """
        :param pseudo: user's nickname
        :return: list of user's tickets
        """
        ticket_list = session.query(TICKET).filter(TICKET.username_user == pseudo).all()
        session.commit()
        return ticket_list

    @staticmethod
    def is_username_available(pseudo: str) -> bool:
        username = db.session.query(USER).filter(USER.username_user == pseudo).first()
        db.session.commit()
        return True if username is None else False
