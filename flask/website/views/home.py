from flask import (
    Blueprint,
    render_template,
    session,
    redirect,
    url_for
)
from flask_mobility.decorators import mobile_template

mod = Blueprint('home', __name__)

@mod.route('/home/', methods=['GET', 'POST'])
@mobile_template('{mobile/Authentification/}home.html')
def home(template):
    return render_template(template)


@mod.route('/home/user/<string:user_id>', methods=['GET'])
def get_user_by_id(user_id):
    return ""


@mod.route('/home/admin', methods=['GET'])
def admin():
    return
