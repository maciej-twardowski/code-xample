from flask import (
	Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from xample.auth import login_required
from xample.db import get_db
from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField
from wtforms.validators import DataRequired


class LinksToDisplayForm(FlaskForm):
	tech = SelectField('Technology', validators=[DataRequired()], id='sel_tech')
	diff = SelectField('Difficulty', validators=[DataRequired()], id='sel_diff')
	submit = SubmitField('Display links')


bp = Blueprint('posts', __name__)



@bp.route('/')
def index():
	db = get_db()

	technologies = db.execute(
		'SELECT id, name '
		'FROM technology '
		'ORDER BY name '
	).fetchall()

	difficulties = db.execute(
		'SELECT id, name '
		'FROM difficulty '
		'ORDER BY id '
	).fetchall()

	form = LinksToDisplayForm()
	form.tech.choices = [('', '')] + technologies
	form.diff.choices = [('', '')] + difficulties

	return render_template('posts/index.html', form=form)

@bp.route('/add_link', methods=('GET', 'POST'))
@login_required
def add_link():
	# if request.method == 'POST':
	# 	title = request.form['title']
	# 	body = request.form['body']
	# 	error = None

	# 	if not title:
	# 		error = 'Title is required.'

	# 	if error is not None:
	# 		flash(error)
	# 	else:
	# 		db = get_db()
	# 		db.execute(
	# 			'INSERT INTO post (title, body, author_id)'
	# 			' VALUES (?, ?, ?)',
	# 			(title, body, g.user['id'])
	# 		)
	# 		db.commit()
	# 		return redirect(url_for('blog.index'))
	# 
	# return render_template('blog/create.html')
	return 'TODO'

@bp.route('/display', methods=('GET', 'POST'))
@login_required
def display():
	return 'TODO'
