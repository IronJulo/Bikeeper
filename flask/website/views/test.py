from flask import Blueprint
from ..models import ORM
from flask_mobility.decorators import mobile_template

mod = Blueprint('test', __name__)


@mod.route('/test/', methods=['GET'])
def test():
    return "Not implemented yet"


@mod.route('/test/admin/<string:admin_username>/tickets/all', methods=['GET'])
def get_tickets_admin_by_id(admin_username):
    res = "<ul>"
    list_ticket = ORM.get_admin_tickets_by_admin_id(admin_username)
    print("List des tickets : ", list_ticket)
    if list_ticket is not False:
        for ticket in list_ticket:
            res += f"<li><p>ID ticket: {ticket.id_ticket}</p>" \
                   f"<p>Title ticket: {ticket.title_ticket}" \
                   f"<p>Is closed?: {ticket.is_closed_ticket}</p></li>"
        res += "</ul>"
        return res
    elif list_ticket is False:
        return "<h1>Vous n'etes pas admin</h1>"


@mod.route('/test/user/<string:username>/tickets/all', methods=['GET'])
def get_user_tickets_by_id(username):
    res = "<ul>"
    list_ticket = ORM.get_user_tickets(username)

    print("List User tieckets : ", list_ticket)
    print("======================================")
    for t in list_ticket:
        print(t.id_ticket)
        print(t.title_ticket)
        print(t.is_closed_ticket)
    print("======================================")

    for ticket in list_ticket:
        res += f"<li><p>ID ticket: {ticket.id_ticket}</p>" \
               f"<p>Title ticket: {ticket.title_ticket}" \
               f"<p>Is closed?: {ticket.is_closed_ticket}</p></li>"
    res += "</ul>"
    return res


@mod.route("/test/size", methods=["GET"])
def get_space():
    """
    return : size of database in MB
    """
    space = ORM.get_space_used_database()
    return str(space[0].get("Size (MB)"))
