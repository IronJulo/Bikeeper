from ..models import USER
from ..models import ORM
from flask import Blueprint
from flask_mobility.decorators import mobile_template

mod = Blueprint('user', __name__)


@mod.route('/users/<string:user_id>', methods=['GET'])
def user_page(user_id):
    user = ORM.get_user(user_id)
    return f"<p>Username: {user.username_user}</p>" \
           f"<p>Number: {user.num_user}</p>" \
           f"<p>Firstname: {user.firstname_user}</p>" \
           f"<p>Lastname: {user.lastname_user}</p>" \
           f"<p>Email: {user.email_user}</p>" \
           f"<p>Town: {user.town_user}</p>" \
           f"<p>Postal code: {user.postal_code_user}</p>" \
           f"<p>Street: {user.street_user}</p>"
