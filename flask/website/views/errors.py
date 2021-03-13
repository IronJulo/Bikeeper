from flask import (
	Blueprint,
	render_template,
	abort
)
from ..models import ORM
from flask_login import current_user

mod = Blueprint('errors', __name__)


@mod.route("/<path:invalid_path>")
def missing_resource(invalid_path):
	abort(404, description="Resource not found")


@mod.app_errorhandler(404)
def handle_404(err):
	return render_template('404.html',devices = ORM.get_devices_by_username(current_user.username_user)), 404


@mod.app_errorhandler(403)
def handle_403(err):
	return render_template('403.html',devices = ORM.get_devices_by_username(current_user.username_user)), 403

