from flask import Blueprint, render_template, request, redirect, url_for, escape
from flask_login import login_required, logout_user

mod = Blueprint('logout', __name__)


@mod.route("/logout/")
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))
