from flask import (
	Blueprint,
	render_template,
	session,
	redirect,
	abort,
	url_for,
	request
)
from flask_mobility.decorators import mobile_template
from flask_login import login_required, login_user, logout_user, current_user
from functools import wraps
from ..models import ORM

mod = Blueprint('admin', __name__)


def admin_required(f):
	@wraps(f)
	def wrap(*args, **kwargs):
		if not current_user.is_admin_user:
			abort(403, description="Can't access an admin page as user")
		return f(*args, **kwargs)

	return wrap


@mod.route('/admin/access', methods=['GET'])
@mobile_template("{mobile/Admin/}admin_access.html")
@login_required
@admin_required
def admin_access(template):
	return render_template(template)


@mod.route('/admin/home', methods=['GET'])
@mobile_template("{mobile/Admin/}admin_home.html")
@login_required
@admin_required
def admin_home(template):
	return render_template(
		template,
		nb_users=ORM.get_number_of_user(),
		tt_data=ORM.get_space_used_database(),
		nb_ticket=ORM.get_number_open_ticket(),
		nb_bikeeper=ORM.get_number_of_bikeeper()
	)


@mod.route('/admin/support', methods=['GET'])
@mobile_template("{mobile/Admin/}admin_support.html")
@login_required
@admin_required
def admin_support(template):
	return render_template(template)


@mod.route('/admin/platform', methods=["GET"])
@login_required
@admin_required
def platform():
	return render_template('admin_platform.html')
