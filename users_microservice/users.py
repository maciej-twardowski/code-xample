#!flask/bin/python
# Based on https://blog.miguelgrinberg.com/post/restful-authentication-with-flask
import os
from flask import Flask, request, jsonify, url_for
from flask_sqlalchemy import SQLAlchemy
from passlib.apps import custom_app_context as pwd_context
from http import HTTPStatus
from werkzeug.exceptions import BadRequest, NotFound, Conflict

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yet another very secret key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users_db.sqlite'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    def __init__(self, username, password):
        self.username = username
        self.password_hash = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)


@app.route('/', methods=['GET'])
def api_info():
    return jsonify(
        api_description_columns='<method>  | <route> | <arguments>',
        api_description=[
            'POST   | /user                   | username, password',
            'GET    | /user/<username>        | --- ',
            'GET    | /users                  | --- ',
            'POST   | /user/<username>/verify | password'
        ]
    )


@app.route('/user', methods=['POST'])
def new_user():
    username = request.form.get('username')
    password = request.form.get('password')
    if username is None or password is None:
        return BadRequest('Missing arguments. Required: <username>, <password>.')

    if User.query.filter_by(username=username).first() is not None:
        return Conflict('User already exists.')

    user = User(username=username, password=password)
    db.session.add(user)
    try:
        db.session.commit()
    except:
        db.session.rollback()
        raise

    return (
        jsonify(succeded=True, id=user.id, username=user.username),
        HTTPStatus.CREATED.value,
        {'Location': url_for('get_user', username=user.username, _external=True)}
    )


@app.route('/user/<string:username>', methods=['GET'])
def get_user(username):
    user = User.query.filter_by(username=username).first()
    if not user:
        raise NotFound()

    return jsonify(id=user.id, username=user.username)


@app.route('/users', methods=['GET'])
def get_users():
    users_info = [{'id': user.id, 'username': user.username} for user in User.query.all()]
    return jsonify(users_info)


@app.route('/user/<string:username>/verify', methods=['POST'])
def verify(username):
    password = request.form.get('password')
    if password is None:
        return BadRequest('Missing password argument')

    user = User.query.filter_by(username=username).first()
    if user is None:
        return NotFound('Non existent user cannot be verified.'),

    return jsonify(valid=user.verify_password(password))


def init_db():
    if not os.path.exists('users_db.sqlite'):
        db.create_all()

    if User.query.count() == 0:
        initial_users = [
            User(username='admin', password='admin'),
            User(username='test', password='test')
        ]

        for u in initial_users:
            db.session.add(u)

        try:
            db.session.commit()
        except:
            db.session.rollback()
            raise


if __name__ == '__main__':
    init_db()
    app.run(port=5001, debug=True)
