from flask import (
    Blueprint,
    render_template,
    session,
    redirect,
    url_for
)
from flask_mobility.decorators import mobile_template

from ..models import ORM

mod = Blueprint('admin', __name__)


@mod.route('/admin/access', methods=['GET'])
@mobile_template("{mobile/Admin/}admin_access.html")
def admin_access(template):
    return render_template(template)


@mod.route('/admin/home', methods=['GET'])
@mobile_template("{mobile/Admin/}admin_home.html")
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
def admin_support(template):
    return render_template(template)


@mod.route('/admin/humberger', methods=['GET'])
@mobile_template("{mobile/Admin/}humberger_overlay_connected_admin.html")
def humberger_overlay_connected_admin(template):
    return render_template(template)


@mod.route('/admin/dashboard', methods=['GET'])
@mobile_template("{mobile/Admin/}support_dashboard_admin.html")
def support_dashboard_admin(template):
    return render_template(template)
