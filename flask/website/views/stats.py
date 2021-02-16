import json

from flask import (
    Blueprint,
    render_template,
    session,
    redirect,
    url_for,
    request,
    current_app
)
from flask_login import current_user

from ..models import ORM
from flask_mobility.decorators import mobile_template

mod = Blueprint("stats", __name__)


@mod.route('/statistics/', methods=['GET', 'POST'])
@mobile_template('{mobile/User/}stats.html')
def statistics(template):
    search_user = request.form.get('search_user', default=None, type=str)
    username = ''

    devices = ORM.get_devices_by_username(current_user.username_user)
    if search_user is not None:  # ADMIN
        res = ORM.search_user(search_user)[0]
        return render_template(
            template,
            username=res.username_user,
            phone=res.num_user,
            street=res.street_user,
            town=res.town_user,
            devices=devices
        )

    else:
        return render_template(
            template,
            username=username
        )
