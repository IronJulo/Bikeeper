from flask import (
    Blueprint,
    render_template,
    session,
    redirect,
    request,
    url_for
)
from flask_mobility.decorators import mobile_template
from flask_login import login_required

from ..models import ORM

mod = Blueprint('home', __name__)


@mod.route('/home/', methods=['GET', 'POST'])
@mobile_template('{mobile/User/}home.html')
def home(template):
    ip_address = request.remote_addr
    print("IP : ", ip_address)
    ORM.log_ip(ip_address)
    return render_template(template)


@mod.route('/mob/home/', methods=['GET', 'POST'])
def mob_home():
    return render_template("mobile/User/home.html")


@mod.route('/mob/support/', methods=['GET', 'POST'])
def mob_support():
    return render_template("mobile/User/support.html")


@mod.route('/mob/localisation/', methods=['GET', 'POST'])
def mob_localisation():
    return render_template("mobile/User/localisation.html")


@mod.route('/mob/statistic/', methods=['GET', 'POST'])
def mob_statistic():
    return render_template("mobile/User/stats.html")


@mod.route('/home/user/<string:user_id>', methods=['GET'])
def get_user_by_id(user_id):
    return ""


@mod.route('/home/admin', methods=['GET'])
def admin():
    return
