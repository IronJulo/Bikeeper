"""
This module interact directly with the database. It make call to sqlalchemy ORM to deal with tables.
"""
import datetime
from typing import List
from sqlalchemy import func
from flask_login import UserMixin, current_user
from flask import jsonify
from .app import db, session, login_manager


class CONTACT(db.Model):
    """
    Store contacts to call when emergency. Linked to user.
    """
    id_contact = db.Column(db.Integer, primary_key=True, autoincrement=True)
    num_contact = db.Column(db.String(15))
    firstname_contact = db.Column(db.String(42))
    lastname_contact = db.Column(db.String(42))
    profile_picture_contact = db.Column(db.String(42))
    num_device = db.Column(db.String(15), db.ForeignKey("DEVICE.num_device"))
    DEVICE = db.relationship("DEVICE", backref=db.backref("CONTACT", lazy="dynamic"))

    def __init__(self, num_contact, firstname_contact, lastname_contact, profile_picture_contact, num_device):
        self.num_contact = num_contact
        self.firstname_contact = firstname_contact
        self.lastname_contact = lastname_contact
        self.profile_picture_contact = profile_picture_contact
        self.num_device = num_device


class LOG(db.Model):
    """
    Store all activities generated by Bikeepers like Alerts, Moving etc...
    """
    id_log = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content_log = db.Column(db.String(150))
    type_log = db.Column(db.String(20))
    datetime_log = db.Column(db.DateTime())
    exception_log = db.Column(db.String(160))
    num_device = db.Column(db.String(15), db.ForeignKey("DEVICE.num_device"))
    DEVICE = db.relationship("DEVICE", backref=db.backref("LOG", lazy="dynamic"))

    def __init__(self, content_log, type_log, datetime_log, exception_log, num_device):
        self.content_log = content_log
        self.type_log = type_log
        self.datetime_log = datetime_log
        self.exception_log = exception_log
        self.num_device = num_device


class DEVICE(db.Model):
    """
    Store a bikeeper device linked to user
    """
    num_device = db.Column(db.String(15), primary_key=True)
    name_device = db.Column(db.String(42))
    row_parameters_device = db.Column(db.String(200))
    username_user = db.Column(db.String(42), db.ForeignKey("USER.username_user"))
    USER = db.relationship("USER", backref=db.backref("DEVICE", lazy="dynamic"))

    def __init__(self, num_device, name_device, row_parameters_device, user):
        self.num_device = num_device
        self.name_device = name_device
        self.row_parameters_device = row_parameters_device
        self.username_user = user

    def set_row_parameters(self, parameters):
        self.row_parameters_device = parameters
        db.session.commit()


class USER(db.Model, UserMixin):
    """
    Store User accounts, username, password, phone number and other...
    """
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
    """
    Store messages linked to tickets
    """
    id_message = db.Column(db.Integer, primary_key=True, autoincrement=True)
    is_admin_message = db.Column(db.Integer, nullable=False)
    datetime_message = db.Column(db.DateTime(), nullable=False)
    content_message = db.Column(db.String(1000), nullable=False)
    username_user = db.Column(db.String(42), db.ForeignKey("USER.username_user"))
    id_ticket = db.Column(db.Integer, db.ForeignKey("TICKET.id_ticket"))
    TICKET = db.relationship("TICKET", backref=db.backref("MESSAGE", lazy="dynamic"))

    def __init__(self, is_admin_message, datetime_message, content_message, id_ticket, username_user):
        self.is_admin_message = is_admin_message
        self.datetime_message = datetime_message
        self.content_message = content_message
        self.id_ticket = id_ticket
        self.username_user = username_user

    def __repr__(self):
        return "<MESSAGE(isadmin='%s', content_message='%s', id_ticket='%s')>" % (
            self.is_admin_message, self.content_message, self.id_ticket)


class TICKET(db.Model):
    """
    Store tickets to user support
    """
    id_ticket = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title_ticket = db.Column(db.String(100), nullable=False)
    is_closed_ticket = db.Column(db.Integer, nullable=False)
    username_user = db.Column(db.String(42), db.ForeignKey("USER.username_user"))
    USER = db.relationship("USER", backref=db.backref("TICKET", lazy="dynamic"))

    def __init__(self, title_ticket, is_closed_ticket, user):
        self.is_closed_ticket = is_closed_ticket
        self.title_ticket = title_ticket
        self.username_user = user


class IPLogger(db.Model):
    """
    Save IPs request by time.
    """
    __tablename__ = "IPLOGGER"
    ip_address = db.Column(db.String(100), nullable=False, primary_key=True)
    time_info = db.Column(db.DateTime(), nullable=False, primary_key=True)

    def __init__(self, ip, time_info):
        self.ip_address = ip
        self.time_info = time_info


class ORM:
    """
    Functions to process database actions
    """

    @staticmethod
    @login_manager.user_loader
    def load_user(username: str):
        """
        Load the user by username
        :params : username str
        """
        return USER.query.filter(USER.username_user == username).first()

    @staticmethod
    def get_users():
        """
        Get all users stored in database
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
        result_proxy = session.execute(query)

        tables_dict, tables = {}, []
        for row_proxy in result_proxy:
            for column, value in row_proxy.items():
                # build up the dictionary
                tables_dict = {**tables_dict, **{column: value}}
            tables.append(tables_dict)

        return str(round(tables_dict['Size (MB)'],2))

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
    def get_number_open_ticket():
        """
        :return: number of opened tickets,
        """
        res = session.query(func.count(TICKET.id_ticket)) \
            .filter(TICKET.is_closed_ticket == 0) \
            .first()
        db.session.commit()
        return res[0]

    @staticmethod
    def get_number_of_user():
        """
        :return: number of users,
        """
        res = session.query(func.count(USER.username_user)) \
            .filter(USER.is_admin_user == 0) \
            .first()
        db.session.commit()
        return res[0]

    @staticmethod
    def get_number_of_bikeeper():
        """
        :return: number of Bikeepers,
        """
        res = session.query(func.count(DEVICE.num_device)) \
            .first()
        print("Bikeepers : ")
        print(res[0])
        db.session.commit()
        return res[0]

    @staticmethod
    def get_message_by_ticket_id(ticket_id):
        """
        :params : ticket_id
        :return: json with messages,
        """

        res = MESSAGE.query \
            .join(TICKET) \
            .filter(MESSAGE.id_ticket == ticket_id) \
            .all()
        db.session.commit()
        messages = {}

        i = 0
        for message in res:
            messages[i] = {
                "content": message.content_message,
                "datetime_message": message.datetime_message.strftime("%m/%d/%Y, %H:%M:%S"),
                "id_ticket": message.id_ticket,
                "is_admin_message": message.is_admin_message,
                "username_user": message.username_user,
                "other_user_picture": ORM.get_other_user_picture_from_ticket_id(message.id_ticket)
            }

            i += 1

        return messages

    @staticmethod
    def messages_to_json(messages):
        return jsonify(messages)

    @staticmethod
    def get_open_ticket():
        """
        :return: opened tickets,
        """
        res = session.query(TICKET).filter(TICKET.is_closed_ticket == 0).all()
        db.session.commit()
        return res

    @staticmethod
    def get_open_ticket_user(username):
        """
        :params: username : str , is the wanted user
        :return user ticket list with only opened tickets
        """
        res = db.session.query(TICKET).join(USER).filter(
            USER.username_user == username,
            TICKET.is_closed_ticket == 0
        ).all()
        return res

    @staticmethod
    def get_picture_message_from_username(username):
        res = db.session.query(USER.profile_picture_user) \
        .join(MESSAGE) \
        .filter(MESSAGE.username_user == username) \
        .first()

        if res:
            return ''.join(res)

        return ''.join(db.session.query(USER.profile_picture_user) \
            .filter(USER.username_user == username) \
            .first())

    @staticmethod
    def get_users_from_ticket_id(id_ticket):
        """
        :params : id_ticket
        :return user present in ticket
        """
        return db.session.query(USER).join(TICKET).filter(TICKET.id_ticket == id_ticket).all()

    @staticmethod
    def get_other_user_picture_from_ticket_id(id_ticket) -> str:
        """
        :params : id_ticket
        :return profile_picture_user is a string
        """
        users = ORM.get_users_from_ticket_id(id_ticket)
        for user in users:
            if user != current_user:
                return user.profile_picture_user
        return "None"  # if errors

    @staticmethod
    def new_contact(num_contact, firstname_contact, lastname_contact, profile_picture_contact, num_device):
        CONTACT(num_contact, firstname_contact, lastname_contact, profile_picture_contact, num_device)
        db.session.commit()

    @staticmethod
    def new_log(content_log, type_log, datetime_log, exception_log, num_device):
        LOG(content_log, type_log, datetime_log, exception_log, num_device)
        db.session.commit()

    @staticmethod
    def new_user(username, password, num, firstname, lastname, email, town, postal_code, street, profile_picture,
                 is_admin):
        # TODO check if it works
        USER(username, password, num, firstname, lastname, email, town, postal_code, street, profile_picture, is_admin)
        db.session.commit()

    @staticmethod
    def new_device(num_device, name_device, row_parameters_device, username):
        # TODO check if it works
        DEVICE(num_device, name_device, row_parameters_device, username)
        db.session.commit()

    @staticmethod
    def new_message(username_user, is_admin_message, datetime_message, content_message, id_ticket):
        # TODO check if it works
        MESSAGE(username_user, is_admin_message, datetime_message, content_message, id_ticket)
        db.session.commit()

    @staticmethod
    def new_ticket(title_ticket, is_closed_ticket, user):
        # TODO check if it works
        TICKET(title_ticket, is_closed_ticket, user)
        db.session.commit()

    @staticmethod
    def log_ip(ip_address):
        """
        Store ip connections in database
        :params : ip
        """
        db.session.add(IPLogger(ip_address, datetime.datetime.now()))
        db.session.commit()

    @staticmethod
    def remove_device(device_id: str) -> bool:
        num_del_rows = db.session.query(DEVICE).filter_by(id=device_id).delete()
        db.session.commit()
        return True if num_del_rows >= 1 else False

    @staticmethod
    def get_device(device_id: str) -> DEVICE:
        return db.session.query(DEVICE).filter_by(id=device_id)