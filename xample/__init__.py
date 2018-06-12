import os
import sys
from flask import Flask
from flask_debugtoolbar import DebugToolbarExtension
from flask_login import LoginManager

basedir = os.path.abspath(os.path.dirname(__file__))

# create and configure the app
app = Flask(__name__)
app.config.from_mapping(
    SECRET_KEY='dev',
    # DEBUG_TB_PROFILER_ENABLED=True,
)

login_manager = LoginManager()
login_manager.init_app(app)
toolbar = DebugToolbarExtension(app)

from . import auth


@login_manager.user_loader
def load_user(username):
    u = auth.User(username)
    return u if u.is_registered() else None


app.register_blueprint(auth.bp)

from . import posts

app.register_blueprint(posts.bp)
app.add_url_rule('/', endpoint='index')
