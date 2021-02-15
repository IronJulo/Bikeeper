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
    return jsonify(
        type_message="ok"
    )


def error(err):
    return jsonify(
        type_message="error",
        error=err
    )


@mod.route('/api/sms/add/', methods=['POST'])
def send_sms_to_bd():
    payload = request.json
    print(payload)
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
    else:
        return error("Schema type not supported")
    ORM.new_log(json.dumps(dic), header['schema'], datetime.now(), exception_log, header['sender'])
    return ok()


@mod.route('/api/bikeeper/add/', methods=['POST'])
def add_bikeeper_to_bd():
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
    if ORM.remove_device(device_id):
        return ok()
    else:
        return error("No rows deleted")


@mod.route('/api/bikeeper/settings/<int:device_id>/update/', methods=['POST'])
def update_bikeeper_settings_to_bd(device_id):
    data = request.json
    ORM.get_device(device_id).set_row_parameters(f"{data}")
    return ok()


@mod.route('/api/bikeeper/currentphone/<string:device_id>/', methods=['GET'])
def get_current_user_phone_from_db(device_id):
    current_phone = ORM.get_associated_phone(device_id)
    return jsonify(
        type_message="response_current_phone",
        current_phone=current_phone
    )


@mod.route('/api/bikeeper/contacts/<string:device_id>/', methods=['GET'])
def get_current_user_contacts(device_id):
    res = []
    contacts = ORM.get_contacts(device_id)
    for contact in contacts:
        res.append(contact.serialize())
    return jsonify(res)
