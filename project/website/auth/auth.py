from flask import  Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, login_user, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from ..models import User, db

auth = Blueprint(
    "auth",
    __name__,
    template_folder="templates",
    static_folder = "static",
    static_url_path="/auth/static"
)


@auth.route('/login', methods = ['POST', 'GET'])
def login():
    if request.method == "POST":
        name = request.form.get("name")
        password = request.form.get("password")
        user = User.query.filter_by(name = name).first()
        if user:
            if check_password_hash(user.password, password):
                login_user(user, remember=True)
                print(f"name: {name}, password: {password}")
                return redirect(url_for('view.home'))
            else:
                flash("Błędna nazwa, lub hasło", category='error')
        else:
            flash("Nazwa nie istnieje", category='error')
    return render_template("login.html")

@auth.route('/register',  methods = ['POST', 'GET'])
def register():
    if request.method == "POST":
        name = request.form.get("name")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")

        user = User.query.filter_by(name=name).first()
        if user:
            flash("Użytkownik już istnieje", category='error')
        elif len(name)<2:
            flash("Nazwa musi zawierać co najmniej dwa znaki", category='error')
        elif len(password1)<6:
            flash("Hasło musi być dłuższe niż 5 znaków", category='error')
        elif password1 != password2:
            flash("Podałeś różne hasła", category='error')
        else:
            new_user = User(name = name, password=generate_password_hash(password1, method='pbkdf2:sha256'))
            db.session.add(new_user)
            db.session.commit()
            print(f"name: {name}, password: {password1}")
            login_user(new_user, remember=True)
            return redirect(url_for('view.home'))
    return render_template("register.html")

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    print("logged out")
    return redirect(url_for('auth.login'))