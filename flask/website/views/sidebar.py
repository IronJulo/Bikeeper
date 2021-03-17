from flask import (
    Blueprint,
    render_template,
    session,
    redirect,
    abort,
    url_for,
    request
)
from flask_mobility.decorators import mobile_template
from ..models import ORM
from flask_login import current_user, login_required
from functools import wraps

mod = Blueprint('sidebar', __name__)

def admin_forbidden(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if current_user.is_admin_user:
            abort(403, description="Admin forbidden")
        return f(*args, **kwargs)
    return wrap

@mod.route("/sidebar/device/change/", methods=['GET', 'POST'])
@admin_forbidden
@login_required
def sidebar_device_change():
    number = request.form.get("device_change")
    user = current_user.username_user
    ORM.update_user_selected_device(number, user)
    return redirect(request.referrer)

