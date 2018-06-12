from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yet another very secret key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users_db.sqlite'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)

from users_microservice import users

db.init_app(app)
users.init_db()
