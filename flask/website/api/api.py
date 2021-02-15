import json

from flask import (
    Blueprint,
    render_template,
    session,
    redirect,
    url_for,
    jsonify,
    request
)
from ..models import ORM
from datetime import datetime

mod = Blueprint('api', __name__)


def ok():
    """
    return ok message

    :return: OK message
    :rtype: Response
    """
    return jsonify(
        type_message="ok"
    )


def error(err):
    """
    return error message

    :param err: Error content
    :type err: string
    :return: error message
    :rtype: Response
    """
    return jsonify(
        type_message="error",
        error=err
    )


@mod.route('/api/sms/add/', methods=['POST'])
def send_sms_to_bd():
    """
    sends sms to the bd
    This sends a SMS to the database.

    :return: Ok message if it worked, error message otherwise
    :rtype: Response
    """
    payload = request.json
    header = payload['header']  # {"key": "[bk]", "schema": "@", "sender": "06...."}
    data = payload['data']
    exception_log = ""
    if header['schema'] == 'W':  # Alert
        dic = {
            "type": data['type'],
            "longitude": data['longitude'],
            "latitude": data['latitude'],
            "charge": data['charge'],
            "level": data['level']
        }
    elif header['schema'] == '@':  # Position
        dic = {
            "longitude": data['longitude'],
            "latitude": data['latitude'],
            "charge": data['charge'],
            "level": data['level'],
            "speed": data['speed'],
            "angle": data['angle']
        }
    elif header['schema'] == '*':  # Normal
        dic = {
            "longitude": data['longitude'],
            "latitude": data['latitude'],
            "charge": data['charge'],
            "level": data['level']
        }
    elif header['schema'] == '+':  # State update
        dic = {
            "type": data['type']
        }
    else:
        return error("Schema type not supported")
    ORM.new_log(json.dumps(dic), header['schema'], datetime.now(), exception_log, header['sender'])
    return ok()


@mod.route('/api/bikeeper/add/', methods=['POST'])
def add_bikeeper_to_bd():
    """
    Adds bikeeper to the database
    This adds a new bikeeper device to the database.

    :return: Ok message if it worked, error message otherwise
    :rtype: Response
    """
    data = request.json
    try:
        num = data['num_device']
        name = data['name_device']
        row_parameters = data['row_parameters_device']
        username = data['username']
    except KeyError as keyerror:
        return error(f"{keyerror}")
    ORM.new_device(num, name, row_parameters, username)
    return ok()


@mod.route('/api/bikeeper/add_raw/', methods=['POST'])
def add_raw_bikeeper_to_bd():
    """
    Adds raw bikeeper to the database
    This adds a bikeeper with raw parameters to the database.

    :return: Ok message if it worked, error message otherwise
    :rtype: Response
    """
    data = request.json
    try:
        num = data['num_device']
        name = data['name_device']
        row_parameters = ""
        username = data['username']
    except KeyError as keyerror:
        return error(f"{keyerror}")
    ORM.new_device(num, name, row_parameters, username)
    return ok()


@mod.route('/api/bikeeper/remove/<int:device_id>/', methods=['DELETE'])
def remove_bikeeper(device_id):
    """
    Removes selected device
    This removes the current device from the database using ORM function.

    :param device_id: id of current device
    :type device id: string
    :return: Ok message if it worked, error message otherwise
    :rtype: Response
    """
    if ORM.remove_device(device_id):
        return ok()
    else:
        return error("No rows deleted")


@mod.route('/api/bikeeper/settings/<int:device_id>/update/', methods=['POST'])
def update_bikeeper_settings_to_bd(device_id):
    """
    Update current device settings to the database
    This updates settings of the device on the database using ORM function.

    :param device_id: id of the current device
    :type device_id: string
    :return: Ok message
    :rtype: Response
    """
    data = request.json
    ORM.get_device(device_id).set_row_parameters(f"{data}")
    return ok()


@mod.route('/api/bikeeper/currentphone/<string:device_id>/', methods=['GET'])
def get_current_user_phone_from_db(device_id):
    """
    Gets current user associated phone
    This gets the current user phone associated on the database from ORM and returns it.

    :param device_id: id of the current device
    :type device_id: string
    :return: Associated phone number of current device
    :rtype: Response
    """
    current_phone = ORM.get_associated_phone(device_id)
    return jsonify(
        type_message="response_current_phone",
        current_phone=current_phone
    )


@mod.route('/api/bikeeper/contacts/<string:device_id>/', methods=['GET'])
def get_current_user_contacts(device_id):
    """
    Gets current user contacts
    This gets current user contacts from ORM and returns it.

    :param device_id: id of the current device
    :type device_id: string
    :return: Contacts of current device
    :rtype: Response
    """
    res = []
    contacts = ORM.get_contacts(device_id)
    for contact in contacts:
        res.append(contact.serialize())
    return jsonify(res)


@mod.route('/api/bikeeper/get_user_num/<string:device_id>/', methods=['GET'])
def get_bikeeper_user_num(device_id):
    """
        Gets bikeeper's owner number
        This gets the number of the bikeeper's owner and returns it.

        :param device_id: id of the current device
        :return: user number str
        :rtype: Response
        """
    try:
        user_num = ORM.get_bikeeper_user_num(device_id)
    except AttributeError:
        return error("Device number not found")
    return jsonify(
        type_message="reponse_num",
        numero=user_num
    )
