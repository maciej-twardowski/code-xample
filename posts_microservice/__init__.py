from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yet another very secret key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts_db.sqlite'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)
db.init_app(app)

from posts_microservice import models, posts

models.init_db()

