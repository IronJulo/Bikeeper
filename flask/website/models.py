from .app import db
from .app import session
from typing import List

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


class USER(db.Model):
    username_user = db.Column(db.String(42), primary_key=True)
    num_user = db.Column(db.String(15))
    firstname_user = db.Column(db.String(42))
    lastname_user = db.Column(db.String(42))
    email_user = db.Column(db.String(42))
    town_user = db.Column(db.String(42))
    postal_code_user = db.Column(db.String(10))
    street_user = db.Column(db.String(42))


class MESSAGE(db.Model):
    id_message = db.Column(db.Integer, primary_key=True)
    is_admin_message = db.Column(db.Integer)
    datetime_message = db.Column(db.DateTime())
    title_message = db.Column(db.String(100))
    content_message = db.Column(db.String(1000))
    id_ticket = db.Column(db.Integer, db.ForeignKey("TICKET.id_ticket"))
    TICKET = db.relationship("TICKET", backref=db.backref("MESSAGE", lazy="dynamic"))


class TICKET(db.Model):
    id_ticket = db.Column(db.Integer, primary_key=True)
    is_closed_ticket = db.Column(db.Integer)
    username_user = db.Column(db.String(42), db.ForeignKey("USER.username_user"))
    USER = db.relationship("USER", backref=db.backref("TICKET", lazy="dynamic"))


def orm_get_user(pseudo: str) -> USER:
    """
    :param pseudo: user's nickname
    :return: USER: user instance
    """
    user = session.query(USER).get(pseudo)
    session.commit()
    return user


def orm_get_user_tickets(pseudo: str) -> List[TICKET]:
    """
    :param pseudo: user's nickname
    :return: list of user's tickets
    """
    ticket_list = session.query(TICKET).filter(TICKET.username_user == pseudo)
    session.commit()
    return ticket_list


def orm_get_user_message_title(ticket: int) -> str:
    """
    :param ticket:
    :return: list of user's tickets
    """
    message = session.query(MESSAGE).filter(MESSAGE.id_ticket == ticket)[0]
    session.commit()
    return message.title_message
