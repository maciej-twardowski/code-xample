from flask import (
	Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from xample.auth import login_required
from xample.db import get_db
from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField
from wtforms.validators import DataRequired, Optional


class LinksToDisplayForm(FlaskForm):
	tech = SelectField('Technology', validators=[], coerce=str) # Optional()
	diff = SelectField('Difficulty', validators=[], coerce=str)
	submit = SubmitField('Display links')


bp = Blueprint('posts', __name__)


@bp.route('/')
def index():
	db = get_db()

	technologies = db.execute(
		'SELECT id, name'
		' FROM technology'
		' ORDER BY name '
	).fetchall()

	difficulties = db.execute(
		'SELECT id, name'
		' FROM difficulty'
		' ORDER BY id'
	).fetchall()

	form = LinksToDisplayForm(csrf_enabled=False)
	form.tech.choices = [('', '')] + technologies
	form.diff.choices = [('', '')] + difficulties

	return render_template('posts/index.html', form=form)


@bp.route('/add_link', methods=['POST'])
@login_required
def add_link():
	return 'TODO'


@bp.route('/display/')
def display_posts():
	tech = request.args.get('tech')
	diff = request.args.get('diff')
	tech = None if tech == '' else tech
	diff = None if diff == '' else diff

	db = get_db()
	posts_headers = db.execute(
		'SELECT id, title, likes'
		' FROM post p '
		' WHERE (technology = ?1 OR ?1 ISNULL) AND' 
		'  (difficulty = ?2 OR ?2 ISNULL)'
		' ORDER BY likes desc', (tech, diff)
	).fetchall()
	# return 'tech:{}, diff:{}'.format(tech, diff)
	return render_template('posts/display.html', posts_headers=posts_headers)


def get_post(id):
    post = get_db().execute(
        'SELECT *'
        ' FROM post p'
        ' WHERE id = ?', (id,)
    ).fetchone()

    if post is None:
        abort(404, "Post id {0} doesn't exist.".format(id))

    return post


@bp.route('/display/<int:post_id>')
def display_post(post_id):
	post = get_post(post_id)
	return str([str(col) for col in post])
