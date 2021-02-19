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
from ..utils import Utils
from flask_login import current_user
from werkzeug.utils import secure_filename
from ..app import app
import os
import imghdr
import hashlib
from random import randint
from flask_login import current_user, login_required
from hashlib import sha256
from flask.helpers import flash

mod = Blueprint('settings', __name__)


@mod.route('/settings/', methods=['GET'])
@mobile_template("{mobile/Settings/}settings.html")
@login_required
def settings(template):
    devices = ORM.get_devices_by_username(current_user.username_user)
    return render_template(
        template,
        devices = devices
    )


"""
ACCOUNT
"""


@mod.route('/settings/account/', methods=['GET'])
@mobile_template("{mobile/Settings/}account.html")
@login_required
def settings_account(template):
    files = os.listdir(app.config['UPLOAD_PATH'])
    devices = ORM.get_devices_by_username(current_user.username_user)
    subscription_name = ORM.get_subscription_name_by_username(current_user.username_user)
    
    return render_template(
        template,
        devices = devices,
        files = files,
        subscription_name = subscription_name,
    )


@mod.route('/settings/account/update/', methods=['POST'])
@login_required
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

    confirmpassword = Utils.get_encrypt_password(request.form.get("confirmpassword"))
    password = ORM.get_password_user_by_username(current_user.username_user)
    if confirmpassword == password:
        validation, message = Utils.is_valid_change_account(mdp, tel, mail, ville, rue, code)
        if validation:
            ORM.update_user(mdp, tel, first, last, mail, ville, code, rue)
            flash(message, "success")
            return redirect(url_for('settings.settings_account'))

        flash(message, "error")
        return redirect(url_for('settings.settings_account'))
        
    flash("Incorrect Password. Changes were not applied!","error")
    return redirect(url_for("settings.settings_account"))
   


'''
DEVICES
'''


@mod.route('/settings/device/', methods=['GET'])
@mobile_template("{mobile/Settings/}device.html")
@login_required
def settings_devices(template):
    devices = ORM.get_devices_by_username(current_user.username_user)
    selected = ORM.get_current_name_device_by_username(current_user.username_user)

    return render_template(
        template,
        devices = devices,
        selected_device = selected
    )


@mod.route('/settings/devices/update/', methods=['GET','POST'])
@login_required
def settings_devices_update():
    name = request.form.get("name")
    movement = request.form.get("movement")
    delay = request.form.get("delay")

    confirmpassword = Utils.get_encrypt_password(request.form.get("confirmpassword"))
    password = ORM.get_password_user_by_username(current_user.username_user)
    if confirmpassword == password:
        ORM.update_device_parameters(current_user.username_user, name)
        flash("Changes have been applied!","success")
        return redirect(url_for("settings.settings_devices"))
    flash("Incorrect Password. Changes were not applied.","error")
    return redirect(url_for("settings.settings_devices"))


'''
CONTACT
'''


@mod.route('/settings/contacts/', methods=['GET'])
@mobile_template("{mobile/Settings/}contacts.html")
@login_required
def settings_contact(template):
    contacts = ORM.get_contacts_by_user(current_user.username_user)
    devices = ORM.get_devices_by_username(current_user.username_user)
    number_contacts = ORM.get_number_of_contacts_by_username(current_user.username_user)

    return render_template(
        template, 
        contacts = contacts, 
        devices = devices,
        number = number_contacts
        )


@mod.route('/settings/contacts/update/', methods=['GET', 'POST'])
@mobile_template("{mobile/Settings/}update_contact.html")
@login_required
def settings_contact_update(template):
    result = request.form
    id_contact = result["id-contact"]
    action = result["action"]
    if action == "edit":
        contact = ORM.get_contact_by_id(id_contact)
        first = contact.firstname_contact
        last = contact.lastname_contact
        tel = contact.num_contact
        devices = ORM.get_devices_by_username(current_user.username_user)
        return render_template(template, id_contact=id_contact, first=first, last=last, tel=tel,
                               devices=devices)

    ORM.remove_contact(id_contact)
    return redirect(url_for('settings.settings_contact'))


@mod.route('/settings/contacts/update/check/', methods=['GET', 'POST'])
@login_required
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
@login_required
def settings_contact_add(template):
    devices = ORM.get_devices_by_username(current_user.username_user)
    return render_template(template, devices=devices)


@mod.route('/settings/contacts/add/check/', methods=['GET', 'POST'])
@login_required
def settings_contact_add_check():
    result = request.form
    first = result['first-name']
    last = result['last-name']
    tel = result['phone']
    device = ORM.get_current_num_device_by_username(current_user.username_user)
    img = '/static/pc/assets/avatar.png'
    
    ORM.new_contact(tel, first, last, img, device)
    flash("Contact has been added.","success")
    return redirect(url_for("settings.settings_contact"))


'''
CREDIT CARD MOBILE
'''


@mod.route('/settings/card/', methods=['GET'])
@mobile_template("{mobile/Settings/}credit-card.html")
@login_required
def settings_card(template):
    return render_template(template)


'''
PAYMENT
'''


@mod.route('/settings/payment/', methods=['GET'])
@mobile_template("{mobile/Settings/}payment.html")
@login_required
def settings_payment(template):
    devices = ORM.get_devices_by_username(current_user.username_user)
    return render_template(template, devices=devices) 


@mod.route('/settings/payment/edit/', methods=['GET', 'POST'])
@mobile_template("{mobile/Settings/}edit_payment.html")
@login_required
def settings_payment_edit(template):
    confirmpassword = Utils.get_encrypt_password(request.form.get("confirmpassword"))
    password = ORM.get_password_user_by_username(current_user.username_user)

    if confirmpassword == password:
        devices = ORM.get_devices_by_username(current_user.username_user)
        return render_template(template, devices=devices)

    flash("Incorrect Password.","error")
    return redirect(url_for("settings.settings_payment"))


@mod.route('/settings/payment/edit/check/', methods=['GET', 'POST'])
@login_required
def settings_payment_edit_check():
    number = request.form.get("number")
    holder_name = request.form.get("holder")
    expiration = request.form.get("expiration")
    cvv = request.form.get("cvv")

    confirmpassword = Utils.get_encrypt_password(request.form.get("confirmpassword"))
    password = ORM.get_password_user_by_username(current_user.username_user)

    if confirmpassword == password:
        flash("Payment service is not available for the moment. Changes were not applies.","error")
        return redirect(url_for('settings.settings_payment'))
        
    flash("Payment service is not available for the moment. Changes were not applies.","error")
    return redirect(url_for('settings.settings_payment'))


@mod.route('/settings/subscription/', methods=['GET'])
@mobile_template("{mobile/Settings/}subscription.html")
@login_required
def settings_subscriptions(template):
    devices = ORM.get_devices_by_username(current_user.username_user)
    subscriptions = ORM.get_subscriptions()
    features = Utils.str_collon_to_list(ORM.get_subscriptions_features()[0])
    subscription_name = ORM.get_subscription_name_by_username(current_user.username_user)

    return render_template(
        template,
        devices = devices,
        subscriptions = subscriptions,
        features = features,
        subscription_name = subscription_name
    )


@mod.route('/settings/subscription/update/', methods=['POST'])
@login_required
def settings_subscriptions_update():
    sub = request.form.get('sub')

    confirmpassword = Utils.get_encrypt_password(request.form.get("confirmpassword"))
    password = ORM.get_password_user_by_username(current_user.username_user)

    if confirmpassword == password:
        if sub == "cancel":
            ORM.remove_device(current_user.selected_device)
            if not len(ORM.get_devices_by_username(current_user.username_user)):
                current_user.selected_device = None
                ORM.block_user(current_user.username_user)
            else:
                current_user.selected_device = ORM.get_devices_by_username(current_user.username_user)[0]

            flash("We're sorry to see you leave us.","error")
            return redirect(url_for('logout.logout'))

        ORM.update_subscription_user_by_username(current_user.username_user,sub)
        flash("Subscription has been changed.","success")
        return redirect(url_for('settings.settings'))
        
    flash("Incorrect Password. Changes were not applied.","error")
    return redirect(url_for('settings.settings'))


'''
PROFILE
'''


def validate_image(stream): #TODO move in Utils
    header = stream.read(512)
    stream.seek(0)
    format = imghdr.what(None, header)
    if not format:
        return None
    return '.' + (format if format != 'jpeg' else 'jpg')


@mod.route('/settings/account/', methods=['POST'])
@login_required
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
