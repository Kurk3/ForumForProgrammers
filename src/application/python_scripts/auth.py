from flask import Blueprint, render_template, redirect, url_for, request, flash
from src.application import db
from .models import User
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

auth = Blueprint("auth", __name__)


@auth.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':

        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                print('Logged in!')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                print("Password is incorrect.")
        else:
            print("Email does not exist.")

    return render_template("sign-in.html", user=current_user)


@auth.route("/sign-up", methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get("email")
        username = request.form.get("username")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")

        email_exists = User.query.filter_by(email=email).first()
        username_exists = User.query.filter_by(username=username).first()

        if email_exists:

            print("Email is already in use.")

        elif username_exists:

            print("Username is already in use.")

        elif password1 != password2:

            print("Passwords do not match.")

        elif len(username) < 2:

            print("Username is too short.")

        elif len(password1) < 6:

            print("Password is too short.")

        elif len(email) < 4:

            print("Email is invalid.")
        else:
            new_user = User(email=email, username=username, password=generate_password_hash(password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('User created!')
            return redirect(url_for('views.home'))

    return render_template("sign-up.html", user=current_user)


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("views.home"))
