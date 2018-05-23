from flask import (
	Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from xample.auth import login_required
from xample.db import get_db

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
		'ORDER BY name '
	).fetchall()

	return render_template('posts/index.html',
		technologies=technologies,
		difficulties=difficulties
	)