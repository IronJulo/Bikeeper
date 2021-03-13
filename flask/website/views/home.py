from flask import (
    Blueprint,
    render_template,
    session,
    redirect,
    request,
    url_for
)
from flask_mobility.decorators import mobile_template
from flask_login import login_required, current_user
from ..models import ORM
from ..utils import Utils

mod = Blueprint('home', __name__)


@mod.route('/home/', methods=['GET', 'POST'])
@mobile_template('{mobile/User/}home.html')
@login_required
def home(template):
    ip_address = request.remote_addr
    print("REAL IP ", request.headers['X-Real-IP'])
    ORM.log_ip(ip_address)
    devices = ORM.get_devices_by_username(current_user.username_user)
    selected_device = current_user.selected_device
    return render_template(
        template,
        devices = devices,
        selected_device=selected_device
        )


@mod.route('/localisation/', methods=['GET', 'POST'])
@login_required
def localisation():
    return render_template(
        "mobile/User/localisation.html"
        )
