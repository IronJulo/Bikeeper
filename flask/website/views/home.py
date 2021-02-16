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
    print("IP : ", ip_address)
    ORM.log_ip(ip_address)
    print(ORM.get_new_num_device())
    return render_template(template)

@mod.route('/mob/localisation/', methods=['GET', 'POST'])
def mob_localisation():
    return render_template("mobile/User/localisation.html")
