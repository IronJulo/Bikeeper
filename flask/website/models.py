from .app import db, session, login_manager
from typing import List
from flask_login import UserMixin
from sqlalchemy import func
from flask import jsonify

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

    def __init__(self, id_contact, num_contact, firstname_contact, lastname_contact, profile_picture_contact, device):
        self.id_contact = id_contact
        self.num_contact = num_contact
        self.firstname_contact = firstname_contact
        self.lastname_contact = lastname_contact
        self.profile_picture_contact = profile_picture_contact
        self.num_device = device.num_device
        self.DEVICE = device


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

    def __init__(self, num_device, name_device, row_parameters_device, user):
        self.num_device = num_device
        self.name_device = name_device
        self.row_parameters_device = row_parameters_device
        self.username_user = user.username_user
        self.USER = user


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

    def __repr__(self):
        return "<User(name='%s', email='%s', is_admin_user='%s')>" % (
            self.username_user, self.email_user, self.is_admin_user)


class MESSAGE(db.Model):
    id_message = db.Column(db.Integer, primary_key=True, autoincrement=True)
    is_admin_message = db.Column(db.Integer)
    datetime_message = db.Column(db.DateTime())
    content_message = db.Column(db.String(1000))
    id_ticket = db.Column(db.Integer, db.ForeignKey("TICKET.id_ticket"))
    TICKET = db.relationship("TICKET", backref=db.backref("MESSAGE", lazy="dynamic"))

    def __init__(self, is_admin_message, datetime_message, content_message, ticket):
        self.is_admin_message = is_admin_message
        self.datetime_message = datetime_message
        self.content_message = content_message
        self.id_ticket = ticket.id_ticket,
        self.TICKET = ticket

    def __repr__(self):
        return "<MESSAGE(isadmin='%s', content_message='%s', id_ticket='%s')>" % (
            self.is_admin_message, self.content_message, self.id_ticket)


class TICKET(db.Model):
    id_ticket = db.Column(db.Integer, primary_key=True)
    title_ticket = db.Column(db.String(100))
    is_closed_ticket = db.Column(db.Integer)
    username_user = db.Column(db.String(42), db.ForeignKey("USER.username_user"))
    USER = db.relationship("USER", backref=db.backref("TICKET", lazy="dynamic"))

    def __init__(self, id_ticket, title_ticket, is_closed_ticket, user):
        self.id_ticket = id_ticket
        self.is_closed_ticket = is_closed_ticket
        self.title_ticket = title_ticket
        self.username_user = user.username_user
        self.USER = user


class ORM:
    @staticmethod
    @login_manager.user_loader
    def load_user(username):
        return USER.query.filter(USER.username_user == username).first()

    @staticmethod
    def get_users():
        """
        :return: list of USERs
        """
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
        ticket_list = session.query(TICKET) \
            .join(USER, TICKET.username_user == USER.username_user, isouter=True) \
            .filter(TICKET.username_user == pseudo and USER.is_admin_user == 0) \
            .all()
        session.commit()
        return ticket_list

    @staticmethod
    def is_username_available(pseudo: str) -> bool:
        """
        :param pseudo: user's nickname
        :return: boolean, true if available
        """
        username = db.session.query(USER).filter(USER.username_user == pseudo).first()
        db.session.commit()
        return True if username is None else False

    @staticmethod
    def is_admin(pseudo: str) -> bool:
        """
        :param pseudo: user's nickname
        :return: boolean, true if is admin
        """
        username = db.session.query(USER).filter(USER.username_user == pseudo and USER.is_admin_user == 1).first()
        print("IS ADmin", username)
        if username.is_admin_user is True:
            return True
        else:
            return False

    @staticmethod
    def get_admin_tickets_by_admin_id(pseudo: str):
        """
        :param pseudo: user's nickname
        :return: boolean, true if available
        """
        if ORM.is_admin(pseudo):
            ticket_list = session.query(TICKET).filter(TICKET.username_user == pseudo and USER.is_admin_user == 1).all()
            session.commit()
            return ticket_list
        else:
            # not admin, return false
            return False

    @staticmethod
    def get_space_used_database():
        """
        :param pseudo: user's nickname
        :return: boolean, true if available
        """
        query = "SELECT table_schema AS \"Database\", SUM(data_length + index_length) / 1024 / 1024 AS \"Size (MB)\"" + "FROM information_schema.TABLES" + " WHERE table_schema = 'BIKEEPER' GROUP BY table_schema"
        resultproxy = session.execute(query)

        d, a = {}, []
        for rowproxy in resultproxy:
            # rowproxy.items() returns an array like [(key0, value0), (key1, value1)]
            for column, value in rowproxy.items():
                # build up the dictionary
                d = {**d, **{column: value}}
            a.append(d)

        return a

    @staticmethod
    def get_associated_phone(phone) -> str:
        """
        :param phone: user's nickname
        :return: str,
        """
        res = session \
            .query(USER.num_user) \
            .join(DEVICE) \
            .filter(DEVICE.num_device == phone) \
            .first()

        db.session.commit()
        return res

    @staticmethod
    def get_open_ticket():
        """
        :return: number of opened tickets,
        """
        res = session.query(func.count(TICKET.id_ticket)) \
            .filter(TICKET.is_closed_ticket == 0) \
            .first()
        return res[0]

    @staticmethod
    def get_number_of_user():
        """
        :return: number of users,
        """
        res = session.query(func.count(USER.username_user)) \
            .filter(USER.is_admin_user == 0) \
            .first()
        return res[0]

    @staticmethod
    def get_message_by_ticket_id(ticket_id):
        """
        :params : ticket_id
        :return: number of users,
        """

        res = session.query(MESSAGE) \
            .join(TICKET) \
            .filter(MESSAGE.id_ticket == ticket_id) \
            .all()

        messages = {}
        print(type(res))
        print("*" * 50)
        i = 0
        for message in res:
            messages[i] = {
                "content": message.content_message,
                "datetime_message": message.datetime_message.strftime("%m/%d/%Y, %H:%M:%S"),
                "id_ticket": message.id_ticket,
                "is_admin_message": message.is_admin_message
            }

            i += 1

        print(messages)
        return jsonify(messages)
