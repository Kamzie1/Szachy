from flask import Blueprint, render_template
from flask_login import current_user, login_required
from ..models import User

view = Blueprint(
    "view",
    __name__,
    template_folder="templates",
    static_folder = "static",
    static_url_path="/view/static"
)



@view.route('/')
@login_required
def home():
    users = User.query.all()
    return render_template("home.html", users = users)
