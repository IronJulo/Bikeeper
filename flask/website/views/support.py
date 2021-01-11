from flask import Blueprint
from ..models import ORM

mod = Blueprint('support', __name__)


@mod.route('/support/', methods=['GET'])
def support():
    return "Not implemented yet"


@mod.route('/support/<int:admin_id>/tickets/all', methods=['GET'])
def get_tickets_admin_by_id(admin_id):
    return ""


@mod.route('/support/<string:user_id>/tickets/all', methods=['GET'])
def get_user_tickets_by_id(user_id):
    res = "<ul>"
    list_ticket = ORM.get_user_tickets(user_id)
    for ticket in list_ticket:
        res += f"<li><p>ID ticket: {ticket.id_ticket}</p>" \
               f"<p>Title ticket: {ticket.title_ticket}" \
               f"<p>Is closed?: {ticket.is_closed_ticket}</p></li>"
    res += "</ul>"
    return res
