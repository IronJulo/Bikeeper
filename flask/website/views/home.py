from flask import (
	Blueprint,
	render_template,
	session,
	redirect,
	request,
	url_for,
	abort
)
from flask_mobility.decorators import mobile_template
from flask_login import login_required, current_user
from ..models import ORM
from ..utils import Utils
from functools import wraps

mod = Blueprint('home', __name__)

PROD_MODE = True


def admin_forbidden(f):
	@wraps(f)
	def wrap(*args, **kwargs):
		if current_user.is_admin_user:
			abort(403, description="Admin forbidden")
		return f(*args, **kwargs)

	return wrap


@mod.route('/home/', methods=['GET', 'POST'])
@mobile_template('{mobile/User/}home.html')
@login_required
@admin_forbidden
def home(template):
	if PROD_MODE:  # In production the request ip is the ngnix ip. We forward ip in headers to keep real ip.
		ip_address = request.headers['X-Real-IP']
	else:
		ip_address = request.remote_addr
	ORM.log_ip(ip_address)
	devices = ORM.get_devices_by_username(current_user.username_user)
	selected_device = current_user.selected_device
	return render_template(
		template,
		devices=devices,
		selected_device=selected_device
	)


@mod.route('/localisation/', methods=['GET', 'POST'])
@login_required
@admin_forbidden
def localisation():
	return render_template(
		"mobile/User/localisation.html"
	)
