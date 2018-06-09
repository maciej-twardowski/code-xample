#!flask/bin/python
# Based on https://blog.miguelgrinberg.com/post/restful-authentication-with-flask
import os
from flask import Flask, abort, request, jsonify, url_for
from flask_sqlalchemy import SQLAlchemy
from passlib.apps import custom_app_context as pwd_context

# initialization
app = Flask(__name__)
app.config['SECRET_KEY'] = 'yet another very secret key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users_db.sqlite'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True

db = SQLAlchemy(app)


class User(db.Model):
	__tablename__ = 'users'
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(64), index=True, unique=True, nullable=False)
	password_hash = db.Column(db.String(128))

	def hash_password(self, password):
		# SHA256-Crypt password hash
		self.password_hash = pwd_context.encrypt(password)

	def verify_password(self, password):
		return pwd_context.verify(password, self.password_hash)


@app.route('/', methods=['GET'])
def api_info():
	return jsonify(
		api_requests=[
			'(method | route | arguments)',
			'POST | /user | username, password',
			'GET  | /user/id | --- ',
			'POST | /auth/login | username, password'
		]
	)


@app.route('/user', methods=['POST'])
def new_user():
	username = request.json.get('username')
	password = request.json.get('password')
	if username is None or password is None:
		abort(400)    # missing arguments

	if User.query.filter_by(username=username).first() is not None:
		return jsonify(succeded=False, error='Username already used.'), 400

	user = User(username=username)
	user.hash_password(password)
	db.session.add(user)
	db.session.commit()
	return jsonify(succeded=True, id=user.id, username=user.username), 201, 
	{'Location': url_for('get_user', id=user.id, _external=True)}


@app.route('/user/<int:id>', methods=['GET'])
def get_user(id):
	user = User.query.get(id)
	if not user:
		jsonify(succeded=False, error='User not registered.')

	return jsonify(succeded=True, id=user.id, username=user.username)


@app.route('/users', methods=['GET'])
def get_users():
	users_info = [{'id': user.id, 'username': user.username} for user in User.query.all()]
	return jsonify(users_info)


@app.route('/auth/login', methods=['POST'])
def login():
	username = request.json.get('username')
	password = request.json.get('password')
	if username is None or password is None:
		abort(400)    # missing arguments
	if User.query.filter_by(username=username).first() is None:
		return jsonify(succeded=False)
	else:
		return jsonify({'result': True})


def init_db():
	if not os.path.exists('users_db.sqlite'):
		db.create_all()

	if User.query.count() == 0:
		initial_users = [
			User(username='admin'),
			User(username='test')
		]

		
		for u in initial_users:
			u.hash_password(u.username)
			db.session.add(u)

		try:
		    db.session.commit()
		except:
		    db.session.rollback()
		    raise


if __name__ == '__main__':
	init_db()
	app.run(port=5001, debug=True)