from flask import (
    Blueprint,
    render_template,
    session,
    redirect,
    url_for
)

mod = Blueprint('home', __name__)


@mod.route('/home/', methods=['GET', 'POST'])
def home():
    return render_template("home.html")


@mod.route('/home/user/<string:user_id>', methods=['GET'])
def get_user_by_id(user_id):
    return ""


@mod.route('/home/admin', methods=['GET'])
def admin():
    return
