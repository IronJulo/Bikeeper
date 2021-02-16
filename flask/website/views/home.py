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

mod = Blueprint('home', __name__)

@mod.route('/home/', methods=['GET', 'POST'])
@mobile_template('{mobile/User/}home.html')
def home(template):
    ip_address = request.remote_addr
    ORM.log_ip(ip_address)
    devices = ORM.get_devices_by_username(current_user.username_user)
    return render_template(
        template,
        devices = devices
        )

@mod.route('/mob/localisation/', methods=['GET', 'POST'])
def mob_localisation():
    return render_template("mobile/User/localisation.html")
