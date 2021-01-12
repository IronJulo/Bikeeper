from flask import (
    Blueprint,
    render_template,
    redirect,
    request,
    url_for
)
from flask_mobility.decorators import mobile_template

from wtforms import (
    StringField,
    PasswordField,
    HiddenField
)
from wtforms.validators import DataRequired
from flask_wtf import FlaskForm
from flask_mobility.decorators import mobile_template
from flask_login import login_required, login_user, logout_user, current_user
from ..models import ORM

from hashlib import sha256

mod = Blueprint('login', __name__)


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    next = HiddenField()

    def get_data(self):
        return self.username.data

    def get_authenticated_user(self):
        user = ORM.load_user(self.username.data)
        if user is None:
            return None
        m = sha256()
        m.update(self.password.data.encode())
        passwd = m.hexdigest()
        return user if passwd == user.password_user else None


@mod.route('/login/', methods=['GET', 'POST'])
@mobile_template("{mobile/Authentification/}login.html")
def login(template):
    f = LoginForm()
    if not f.is_submitted():
        f.next.data = request.args.get("next")
    elif f.validate_on_submit():
        user = f.get_authenticated_user()
        if user:
            login_user(user)
            next = f.next.data or url_for("home.home")
            return redirect(next)
    return render_template(
        template,
        form=f,
    )