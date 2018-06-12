import requests
import sys
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from flask_login import current_user, login_user, logout_user, UserMixin
from werkzeug.urls import url_parse
from xample.forms import LoginForm, RegistrationForm
from xample import login_manager
from http import HTTPStatus


class User(UserMixin):
    # todo make this part of the config
    USERS_URL = 'http://127.0.0.1:5001'

    def __init__(self, username):
        self.username = username

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def get_id(self):
        return str(self.username)

    def is_registered(self):
        response = requests.get(f'{self.USERS_URL}/user/{self.username}')
        return True if response.status_code == HTTPStatus.OK.value else False

    def register(self, password):
        registration_data = {'username': self.username, 'password': password}
        response = requests.post(f'{self.USERS_URL}/user', registration_data)
        if response.status_code == HTTPStatus.CREATED.value:
            return True

        return False

    def verify(self, password):
        verification_data = {'password': password}
        response = requests.post(
            f'{self.USERS_URL}/user/{self.username}/verify',
            data=verification_data
        )
        if response.status_code == HTTPStatus.OK.value:
            return response.json()['valid']
        else:
            # user does not exist
            print(response)
            return False


bp = Blueprint('auth', __name__, url_prefix='/auth')


# @login_manager.user_loader
# def load_user(username):
#     u = User(username)
#     return u if u.is_registered() else None
    # try:
    #     return u if u.is_registered() else None
    # except requests.exceptions.ConnectionError:
    #     print("load_user: Users service is unavailable.", file=sys.stderr)
    #     return None


@bp.route('/register', methods=('GET', 'POST'))
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        u = User(form.username.data)
        if u.register(form.password.data):
            flash('Congratulations, you are now a registered user!')
            return redirect(url_for('auth.login'))
        else:
            flash('User already exists :(')

    return render_template('auth/register.html', title='Register', form=form)


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        u = User(form.username.data)
        if not u.is_registered() or not u.verify(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('auth.login'))
        login_user(u)
        flash('Logged in successfully!')

        next_page = request.args.get('next')
        # is_safe(next_page)?
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('auth/login.html', title='Sign In', form=form)


@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))
