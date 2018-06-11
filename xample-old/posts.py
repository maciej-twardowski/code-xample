from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField
from wtforms.validators import DataRequired, Optional
from xample.forms import LinksToDisplayForm
from flask_login import login_required
from xample.user import User, Technology, Difficulty, Post

bp = Blueprint('posts', __name__)


@bp.route('/')
def index():
    technologies = Technology.query.all()
    tech_options = [(tech.id, tech.name) for tech in technologies]
    difficulties = Difficulty.query.all()
    diff_options = [(diff.id, diff.name) for diff in difficulties]

    form = LinksToDisplayForm(csrf_enabled=False)
    form.tech.choices = [('', '')] + tech_options
    form.diff.choices = [('', '')] + diff_options

    return render_template('posts/index.html', form=form)  #


@bp.route('/add_link', methods=['POST'])
@login_required
def add_link():
    return 'TODO'


def alchemy_object_to_dict(obj):
    return dict((col, getattr(obj, col)) for col in obj.__table__.columns.keys())


@bp.route('/display/')
def display_posts():
    tech = request.args.get('tech')
    diff = request.args.get('diff')

    filtered_posts = (
        Post.query
            .filter((Post.technology == tech) | (tech == ''))
            .filter((Post.difficulty == diff) | (diff == ''))
            .all()
    )
    post_dicts = [alchemy_object_to_dict(post) for post in filtered_posts]
    # TODO send only necessary data, display in pretty form
    return render_template('posts/display.html', post_dicts=post_dicts)


@bp.route('/display/<int:post_id>')
def display_post(post_id):
    post = Post.query.get(post_id)

    if post is None:
        abort(404, "Post id {0} doesn't exist.".format(post_id))
    # TODO display in pretty form
    # TODO allow users to like posts
    return str(alchemy_object_to_dict(post))
