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
from flask.helpers import flash

mod = Blueprint("stats", __name__)


@mod.route('/statistics/', methods=['GET', 'POST'])
@mobile_template('{mobile/User/}stats.html')
def statistics(template):
	search_user = request.form.get('search_user', default=None, type=str)

	if search_user is not None:  # ADMIN
		res = ORM.search_user(search_user)
		if len(res)!=0:
			res = res [0]
			devices = ORM.get_devices_by_username(res.username_user)
			price = ORM.get_price_from_subscription_name(res.name_subscription)
					
		else:
			flash("User not found.","error")
			return redirect(url_for('stats.statistics'))

		return render_template(
			template,
			username=res.username_user,
			phone=res.num_user,
			street=res.street_user,
			town=res.town_user,
			devices=devices,
			picture=res.profile_picture_user,
			date=res.date_creation_user,
			subscription=res.name_subscription,
			price=price
		)

	else:
		return render_template(
			template,
			username='',
			devices=ORM.get_devices_by_username(current_user.username_user),
			id_device =current_user.selected_device
		)
