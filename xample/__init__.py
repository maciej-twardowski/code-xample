import os
from flask import Flask
from flask_debugtoolbar import DebugToolbarExtension
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

basedir = os.path.abspath(os.path.dirname(__file__))

# create and configure the app
app = Flask(__name__)
app.config.from_mapping(
	SECRET_KEY='dev',
	# DEBUG_TB_PROFILER_ENABLED=True,
	# todo change location of db
	SQLALCHEMY_DATABASE_URI='sqlite:///' + os.path.join(basedir, 'alchemy_xample.db'),
	SQLALCHEMY_TRACK_MODIFICATIONS=False
)

db = SQLAlchemy(app)
migrate = Migrate(app, db)
login_manager = LoginManager(app)
login_manager.init_app(app)
# login_manager.login_view = 'auth.login'
toolbar = DebugToolbarExtension(app)

from . import models
models.init_db() # add initial users, techs, difficulties and posts

@login_manager.user_loader
def load_user(id):
	return models.User.query.get(int(id))

from . import auth
app.register_blueprint(auth.bp)

from . import posts
app.register_blueprint(posts.bp)
app.add_url_rule('/', endpoint='index')
