from flask import (
    Blueprint,
    render_template,
    session,
    redirect,
    url_for
)
from flask_mobility.decorators import mobile_template
from flask_login import login_required

mod = Blueprint('home', __name__)

@mod.route('/home/', methods=['GET', 'POST'])
# @mobile_template('{mobile/User/}dashboard.html')
def home(template):
    return render_template(template)


@mod.route('/mob/home/', methods=['GET', 'POST'])
def mob_home():
    return render_template("mobile/User/dashboard.html")

@mod.route('/mob/support/', methods=['GET', 'POST'])
def mob_support():
    return render_template("mobile/User/support-chat.html")

@mod.route('/mob/statistic/', methods=['GET', 'POST'])
def mob_localisation():
    return render_template("mobile/User/statistics.html")

@mod.route('/mob/localisation/', methods=['GET', 'POST'])
def mob_statistic():
    return render_template("mobile/User/localisation.html")




@mod.route('/home/user/<string:user_id>', methods=['GET'])
def get_user_by_id(user_id):
    return ""


@mod.route('/home/admin', methods=['GET'])
def admin():
    return
