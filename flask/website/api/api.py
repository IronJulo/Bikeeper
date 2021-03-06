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
    :return: Ok message if it worked, error message otherwise
    :rtype: Response
    """
    if ORM.remove_device(device_id):
        return ok()
    else:
        return error("No rows deleted")


@mod.route('/api/bikeeper/settings/<string:device_id>/update/', methods=['POST'])
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
    user = ORM.get_device(device_id).USER
    return jsonify(
        contacts=res,
        bikeeper_owner=f"{user.firstname_user} {user.lastname_user}"
    )


@mod.route('/api/stats/cpu/', methods=['GET'])
def get_current_cpu_usage():
    """
    Gets current cpu usage
    This gets current cpu usage of the server.

    :rtype: Response
    """
    return jsonify(
        response=ORM.get_current_cpu_usage()
    )


@mod.route('/api/stats/ram/', methods=['GET'])
def get_current_ram_usage():
    """
    Gets current ram usage
    This gets current ram usage of the server.

    :rtype: Response
    """
    return jsonify(
        response=ORM.get_current_ram_usage()
    )


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
        ORM.new_log("{}", "I", datetime.now(), "", device_id)
    except AttributeError:
        return error("Device number not found")
    return jsonify(
        type_message="response_num",
        numero=user_num
    )


@mod.route('/api/bikeeper/get_last_ride_bikeeper/<string:device_id>', methods=['GET'])
def get_last_ride_bikeeper(device_id: str):
    """
    Gets the user's bikeepers that has logs at a given date.

    :param device_id: username of the user
    :return: last ride info
    :rtype: Response
    """
    return jsonify(
        ORM.get_last_ride_info(device_id)
    )


@mod.route('/api/bikeeper/get_rides_bikeeper_from_user_at_time/<string:username>/<string:date>', methods=['GET'])
def get_rides_bikeeper_from_user_at_time(username: str, date: str):
    """
    Gets rides by user and selected date

    :param username: username of the user
    :param date: date
    :return: list of bikeepers id
    :rtype: Response
    """
    return jsonify(
        ORM.get_rides_bikeeper_from_user_at_time(username, date)
    )


@mod.route('/api/bikeeper/get_rides_from_user_at_time_with_bikeeper/<string:username>/<string:device_id>/<string:date>',
           methods=['GET'])
def get_rides_from_user_at_time_with_bikeeper(username: str, device_id: str, date: str):
    """
    Gets a list of rides at a given date, bikeeper and user.

    :param username: username of the user
    :param date: date
    :param device_id: device id
    :return: list of rides
    :rtype: Response
    """
    return jsonify(
        ORM.get_rides_from_user_at_time_with_bikeeper(username, device_id, date)
    )


@mod.route('/api/bikeeper/get_bikeer_name_by_id/<string:device_id>', methods=['GET'])
def get_bikeeper_name_by_id(device_id):
    """
    Gets the device name of a given device

    :param device_id: device id
    :return: name of the device
    :rtype: Response
    """
    device = ORM.get_device(device_id)
    return jsonify(
        device.name_device
    )


@mod.route('/api/bikeeper/get_logs_at_date/<string:device_id>/<string:date>', methods=['GET'])
def get_logs_at_date(device_id, date):
    """
    Get logs corresponding to a date
    :param device_id: device id
    :param date: date
    :rtype: Response
    """
    return jsonify(
        ORM.get_logs_at_date(device_id, date)
    )


@mod.route('/api/current_device/<string:username>', methods=['GET'])
def get_current_selected_device(username):
    """
    Get the current selected device stored in database
    :param username: the current username
    :rtype: Response
    """
    return jsonify(
        response=ORM.get_current_num_device_by_username(username)
    )


@mod.route('/api/user/profile/<string:username>', methods=['GET'])
def get_user_picture(username):
    """
    Get current user picture stored in database
    :param username: the current username
    :rtype: Response
    """
    return jsonify(
        response=ORM.get_user(username).profile_picture_user
    )


@mod.route('/api/contact/profile/<string:contact_id>', methods=['GET'])
def get_contact_picture(contact_id):
    """
    Get current contact picture stored in database
    :param contact_id: the wanted contact_id
    :rtype: Response
    """
    return jsonify(
        response=ORM.get_contact_by_id(contact_id).profile_picture_contact
    )


@mod.route('/api/bikeeper/get_battery_level/<string:device_id>', methods=['GET'])
def get_battery_level(device_id):
    """
    Get current user picture stored in database
    :param device_id: the device_id
    :rtype: Response
    """
    return jsonify(
        ORM.get_battery_lvl(device_id)
    )


@mod.route('/api/bikeeper/search_user/', methods=['GET'])
def search_user():
    """
    Get user research
    :param query: the query
    :rtype: Response
    """
    query = request.args.to_dict()["query"]
    return jsonify(
        suggestions=[{"value": user.username_user} for user in ORM.search_user(query)]
    )


@mod.route('/api/bikeeper/get_last_log_position/<string:device_id>', methods=['GET'])
def get_last_log_position(device_id):
    """
    Get last log that gives the location
    :param device_id: the device id
    :rtype: Response
    """
    log = ORM.get_last_log_position(device_id)
    if log is None:
        return jsonify(
            response="None"
        )
    else:
        return jsonify(
            log.serialize()
        )


@mod.route('/api/test/update_device/<string:username>/<int:id_device>', methods=['POST'])  # TODO replace /test/
def update_current_selected_device(username, id_device):
    """
    Update the current selected device stored in database
    :param username: the current username
    :rtype: Response
    """
    ORM.update_user_selected_device(id_device, username)
    print(ORM.get_current_device_by_username(username))
    return jsonify(response=ORM.get_current_device_by_username(username))


@mod.route("/api/device/<int:id_device>", methods=["GET"])
def is_parked(id_device):
    return jsonify(parked=ORM.is_parked(id_device))
