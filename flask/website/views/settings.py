from flask import (
    Blueprint,
    render_template,
    session,
    redirect,
    url_for,
    request
)
from flask_mobility.decorators import mobile_template
from ..models import ORM
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
def settings_account():
    pseudo = current_user.username_user
    first = current_user.firstname_user
    last = current_user.lastname_user
    mdp = current_user.password_user
    tel = current_user.num_user
    mail = current_user.email_user
    ville = current_user.town_user
    code = current_user.postal_code_user
    rue = current_user.street_user
    return render_template("account.html", pseudo=pseudo, first=first, last=last, mdp=mdp, tel=tel, mail=mail,
                           ville=ville, code=code, rue=rue)


@mod.route('/settings/account/update/', methods=['GET', 'POST'])
def settings_account_update():
    result = request.form
    first = result['first-name']
    last = result['last-name']
    tel = result['phone']
    mail = result['email']
    # image=result['avatar']
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
    return render_template(template)


@mod.route('/settings/devices/update/', methods=['GET'])
def settings_devices_update():
    return redirect(url_for("settings.settings_devices"))


'''
CONTACT
'''


@mod.route('/settings/contacts/', methods=['GET'])
@mobile_template("{mobile/Settings/}contacts.html")
def settings_contact(template):
    contacts=ORM.get_contacts_by_user(current_user.username_user)
    return render_template(template,contacts=contacts)


@mod.route('/settings/contacts/update/', methods=['GET','POST'])
def settings_contact_update():
    result=request.form
    id_contact=result["id-contact"]
    action=result["action"]
    if action=="edit":
        contact=ORM.get_contact_by_id(id_contact)
        first=contact.firstname_contact
        last=contact.lastname_contact
        tel=contact.num_contact
        return render_template("update_contact.html",id_contact=id_contact,first=first,last=last,tel=tel)
    print('-'*100)
    print(id_contact)
    print('-'*100)
    ORM.remove_contact(id_contact)
    return redirect(url_for('settings.settings_contact'))


@mod.route('/settings/contacts/update/check/', methods=['GET', 'POST'])
def settings_contact_update_check():
    result=request.form
    first=result['first-name']
    last=result['last-name']
    tel=result['phone']
    id_contact=result['id-contact']
    ORM.update_contact(tel,first,last,id_contact)
    return redirect(url_for("settings.settings_contact"))


@mod.route('/settings/contacts/add/', methods=['GET'])
@mobile_template('{mobile/Settings/}add_contact.html')
def settings_contact_add(template):
    return render_template(template)


@mod.route('/settings/contacts/add/check/', methods=['GET', 'POST'])
def settings_contact_add_check():
    result=request.form
    first=result['first-name']
    last=result['last-name']
    tel=result['phone']
    device="0664277796"
    img='static/pc/assets/avatar.png'
    ORM.new_contact(tel, first, last, img, device)
    return redirect(url_for("settings.settings_contact"))


# @mod.route('/settings/contacts/remove/', methods=['GET','POST'])
# def settings_contact_remove():
#     result=request.form
#     id_contact=result['id-contact']
#     print(id_contact)
#     ORM.remove_contact(id_contact)
#     return redirect(url_for('settings.settings_contact'))


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
    return render_template(template)


@mod.route('/settings/payment/edit/', methods=['GET', 'POST'])
def settings_payment_edit():
    return render_template('edit_payment.html')


@mod.route('/settings/payment/edit/check/', methods=['GET', 'POST'])
def settings_payment_edit_check():
    return redirect(url_for('settings.settings_payment'))


@mod.route('/settings/subscription/', methods=['GET'])
@mobile_template("{mobile/Settings/}subscription.html")
def settings_subscriptions(template):
    return render_template(template)


@mod.route('/settings/subscription/cancel/', methods=['GET'])
def settings_subscriptions_cancel():
    return redirect(url_for('logout.logout'))


@mod.route('/settings/subscription/change/', methods=['GET'])
def settings_subscriptions_change():
    return redirect(url_for('settings.settings_subscriptions'))
