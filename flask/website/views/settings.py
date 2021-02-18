from flask import (
    Blueprint,
    render_template,
    session,
    redirect,
    send_from_directory,
    url_for,
    request
)
from flask_mobility.decorators import mobile_template
from ..models import ORM
from flask_login import current_user
from werkzeug.utils import secure_filename
from ..app import app
import os
import imghdr
import hashlib
from random import randint
from flask_login import current_user

mod = Blueprint('settings', __name__)


@mod.route('/settings/', methods=['GET'])
@mobile_template("{mobile/Settings/}settings.html")
def settings(template):
    return render_template(
        template
    )


"""
ACCOUNT
"""


@mod.route('/settings/account/', methods=['GET'])
@mobile_template("{mobile/Settings/}account.html")
def settings_account(template):
    files = os.listdir(app.config['UPLOAD_PATH'])
    devices = ORM.get_devices_by_username(current_user.username_user)

    return render_template(
        template,
        devices=devices,
        files=files
    )


@mod.route('/settings/account/update/', methods=['POST'])
def settings_account_update():
    result = request.form
    first = result['first-name']
    last = result['last-name']
    tel = result['phone']
    mail = result['email']
    mdp = result['password']
    code = result['postal-code']
    ville = result['town']
    rue = result['street']
    ORM.update_user(mdp, tel, first, last, mail, ville, code, rue)
    return redirect(url_for('settings.settings_account'))


'''
DEVICES
'''


@mod.route('/settings/device/', methods=['GET'])
@mobile_template("{mobile/Settings/}device.html")
def settings_devices(template):
    devices = ORM.get_devices_by_username(current_user.username_user)
    return render_template(
        template,
        devices=devices
    )


@mod.route('/settings/devices/update/', methods=['GET'])
def settings_devices_update():
    return redirect(url_for("settings.settings_devices"))


'''
CONTACT
'''


@mod.route('/settings/contacts/', methods=['GET'])
@mobile_template("{mobile/Settings/}contacts.html")
def settings_contact(template):
    contacts = ORM.get_contacts_by_user(current_user.username_user)
    devices = ORM.get_devices_by_username(current_user.username_user)
    return render_template(template, contacts=contacts, devices=devices)


@mod.route('/settings/contacts/update/', methods=['GET', 'POST'])
def settings_contact_update():
    result = request.form
    id_contact = result["id-contact"]
    action = result["action"]
    if action == "edit":
        contact = ORM.get_contact_by_id(id_contact)
        first = contact.firstname_contact
        last = contact.lastname_contact
        tel = contact.num_contact
        devices = ORM.get_devices_by_username(current_user.username_user)
        return render_template("update_contact.html", id_contact=id_contact, first=first, last=last, tel=tel,
                               devices=devices)

    ORM.remove_contact(id_contact)
    return redirect(url_for('settings.settings_contact'))


@mod.route('/settings/contacts/update/check/', methods=['GET', 'POST'])
def settings_contact_update_check():
    result = request.form
    first = result['first-name']
    last = result['last-name']
    tel = result['phone']
    id_contact = result['id-contact']
    ORM.update_contact(tel, first, last, id_contact)
    return redirect(url_for("settings.settings_contact"))


@mod.route('/settings/contacts/add/', methods=['GET'])
@mobile_template('{mobile/Settings/}add_contact.html')
def settings_contact_add(template):
    devices = ORM.get_devices_by_username(current_user.username_user)
    return render_template(template, devices=devices)


@mod.route('/settings/contacts/add/check/', methods=['GET', 'POST'])
def settings_contact_add_check():
    result = request.form
    first = result['first-name']
    last = result['last-name']
    tel = result['phone']
    device = "0664277796"
    img = 'static/pc/assets/avatar.png'
    ORM.new_contact(tel, first, last, img, device)
    return redirect(url_for("settings.settings_contact"))


'''
CREDIT CARD MOBILE
'''


@mod.route('/settings/card/', methods=['GET'])
@mobile_template("{mobile/Settings/}credit-card.html")
def settings_card(template):
    return render_template(template)


'''
PAYMENT
'''


@mod.route('/settings/payment/', methods=['GET'])
@mobile_template("{mobile/Settings/}edit_payment.html")
def settings_payment(template):
    devices = ORM.get_devices_by_username(current_user.username_user)
    return render_template(template, devices=devices)


@mod.route('/settings/payment/edit/', methods=['GET', 'POST'])
def settings_payment_edit():
    devices = ORM.get_devices_by_username(current_user.username_user)
    return render_template('edit_payment.html', devices=devices)


@mod.route('/settings/payment/edit/check/', methods=['GET', 'POST'])
def settings_payment_edit_check():
    return redirect(url_for('settings.settings_payment'))


@mod.route('/settings/subscription/', methods=['GET'])
@mobile_template("{mobile/Settings/}subscription.html")
def settings_subscriptions(template):
    devices = ORM.get_devices_by_username(current_user.username_user)
    return render_template(template, devices=devices)


@mod.route('/settings/subscription/cancel/', methods=['GET'])
def settings_subscriptions_cancel():
    return redirect(url_for('logout.logout'))


@mod.route('/settings/subscription/change/', methods=['GET'])
def settings_subscriptions_change():
    return redirect(url_for('settings.settings_subscriptions'))


'''
PROFILE
'''


def validate_image(stream):
    header = stream.read(512)
    stream.seek(0)
    format = imghdr.what(None, header)
    if not format:
        return None
    return '.' + (format if format != 'jpeg' else 'jpg')


@mod.route('/settings/account/', methods=['POST'])
def upload_files():
    if current_user.is_authenticated:

        uploaded_file = request.files['file']
        filename = secure_filename(uploaded_file.filename)
        extention = filename.split(".")
        filename = hashlib.md5((filename + "Bikeeper" + str(randint(0, 9))).encode()).hexdigest() + "." + extention[
            1]  # Salt
        print(filename)

        if filename != "":
            file_ext = os.path.splitext(filename)[1]
            if file_ext not in app.config['UPLOAD_EXTENSIONS'] or file_ext != validate_image(uploaded_file.stream):
                return "Invalid image", 400
            uploaded_file.save(os.path.join(app.config['UPLOAD_PATH'], filename))
            print("new path : ", str(os.path.join(app.config['UPLOAD_PATH'] + filename)))
            ORM.replace_image(current_user.username_user, str(os.path.join(app.config['UPLOAD_PATH'] + filename)))
        return '', 204

    return redirect(url_for('index.index'))
