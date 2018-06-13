from flask import (
    Blueprint, flash, redirect, render_template, request, url_for
)
from xample.forms import LinksToDisplayForm, PostForm
from flask_login import login_required, current_user
from xample.posts_api_handling import get_all_technologies, get_all_difficulties,\
    get_filtered_posts, get_post, create_post
from werkzeug.exceptions import NotFound

bp = Blueprint('posts', __name__)


def get_tech_and_diff_options():
    technologies = get_all_technologies()
    tech_options = [(tech.get('id'), tech.get('name')) for tech in technologies]
    difficulties = get_all_difficulties()
    diff_options = [(diff.get('id'), diff.get('name')) for diff in difficulties]
    return tech_options, diff_options


@bp.route('/')
def index():
    tech_options, diff_options = get_tech_and_diff_options()
    form = LinksToDisplayForm(csrf_enabled=False)
    form.set_tech_options([('', '')] + tech_options)
    form.set_diff_options([('', '')] + diff_options)
    return render_template('posts/index.html', form=form)


@bp.route('/add_link', methods=['GET', 'POST'])
@login_required
def add_link():
    form = PostForm()
    tech_options, diff_options = get_tech_and_diff_options()
    form.set_tech_options(tech_options)
    form.set_diff_options(diff_options)

    # todo validation
    # if form.validate_on_submit():
    if request.method == 'POST':
        result = create_post(
            current_user.username,
            form.title.data,
            form.body.data,
            form.link.data,
            form.tech.data,
            form.diff.data,
        )

        created_post_id = result.get('id')
        return redirect(url_for('posts.display_post', post_id=created_post_id))

    return render_template('posts/add_link.html', form=form)


def alchemy_object_to_dict(obj):
    return dict((col, getattr(obj, col)) for col in obj.__table__.columns.keys())


@bp.route('/display/')
def display_posts():
    tech = request.args.get('tech')
    diff = request.args.get('diff')
    filtered_posts = get_filtered_posts(tech, diff)
    return render_template('posts/display.html', post_dicts=filtered_posts)


@bp.route('/display/<int:post_id>')
def display_post(post_id):
    post = get_post(post_id)
    if post is None:
        return NotFound()
    # TODO allow users to like posts
    return render_template('posts/display_post.html', post=post)
