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
from flask_login import current_user, login_required

mod = Blueprint('sidebar', __name__)

@login_required
@mod.route("/sidebar/device/change/", methods=['GET', 'POST'])
def sidebar_device_change():
    number = request.form.get("device_change")
    user = current_user.username_user
    ORM.update_user_selected_device(number, user)
    return redirect(request.referrer)

    