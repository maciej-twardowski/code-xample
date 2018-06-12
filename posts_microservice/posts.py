# Based on https://blog.miguelgrinberg.com/post/restful-authentication-with-flask
from http import HTTPStatus
from flask import request, jsonify, url_for
from posts_microservice import app, db
from posts_microservice.models import Technology, Difficulty, Post, alchemy_object_to_dict
from werkzeug.exceptions import BadRequest, NotFound


@app.route('/', methods=['GET'])
def api_info():
    return jsonify(
        api_requests=[
            '(method | route | arguments (O - optional)',
            'GET  | /posts | technology(O), difficulty(O)',
            'GET  | /post/id | ---',
            'GET  | /technologies | ---',
            'GET  | /technology/id | ---',
            'GET  | /difficulties | ---',
            'GET  | /difficulty/id | ---',
            'POST | /post  | author_name, title, body, link, technology, difficulty',
            'POST | /post/id/like | ---',
        ]
    )


@app.route('/posts', methods=['GET'])
def get_posts():
    tech_id = request.args.get('tech')
    if tech_id and Technology.query.filter(Technology.id == tech_id).first() is None:
        return BadRequest('Technology not found.')

    diff_id = request.args.get('diff')
    if diff_id and Difficulty.query.filter(Difficulty.id == diff_id).first() is None:
        return BadRequest('Difficulty not found.')

    filtered_posts = (
        Post.query
            .filter((Post.technology == tech_id) | (tech_id == '') | (tech_id is None))
            .filter((Post.difficulty == diff_id) | (diff_id == '') | (diff_id is None))
            .all()
    )
    post_dicts = [alchemy_object_to_dict(post) for post in filtered_posts]
    return jsonify(post_dicts)


@app.route('/post/<post_id>', methods=['GET'])
def get_post(post_id):
    post = Post.query.get(post_id)
    if not post:
        return NotFound()

    return jsonify(alchemy_object_to_dict(post))


@app.route('/technologies', methods=['GET'])
def get_technologies():
    technologies_info = [alchemy_object_to_dict(technology) for technology in Technology.query.all()]
    return jsonify(technologies_info)


@app.route('/technology/<tech_id>', methods=['GET'])
def get_technology(tech_id):
    technology = Technology.query.get(tech_id)
    if not technology:
        return NotFound()

    return jsonify(alchemy_object_to_dict(technology))


@app.route('/difficulties', methods=['GET'])
def get_difficulties():
    difficulties_info = [alchemy_object_to_dict(difficulty) for difficulty in Difficulty.query.all()]
    return jsonify(difficulties_info)


@app.route('/difficulty/<diff_id>', methods=['GET'])
def get_difficulty(diff_id):
    difficulty = Difficulty.query.get(diff_id)
    if not difficulty:
        return NotFound()

    return jsonify(alchemy_object_to_dict(difficulty))


@app.route('/post', methods=['POST'])
def new_post():
    author_name = request.form.get('author_name')
    title = request.form.get('title')
    body = request.form.get('body')
    link = request.form.get('link')
    technology = request.form.get('technology')
    difficulty = request.form.get('difficulty')

    if not all(var is not None for var in [author_name, title, body, link, technology, difficulty]):
        raise BadRequest('Missing arguments.')

    if Technology.query.filter(Technology.id == technology).first() is None:
        raise BadRequest('Technology does not exist.')

    if Difficulty.query.filter(Difficulty.id == difficulty).first() is None:
        raise BadRequest('Difficulty does not exist.')

    post = Post(author_name=author_name, title=title,
                body=body, link=link, technology=technology,
                difficulty=difficulty)

    db.session.add(post)
    try:
        db.session.commit()
    except:
        db.session.rollback()
        raise

    return (
        jsonify(alchemy_object_to_dict(post)),
        HTTPStatus.CREATED.value,
        {'Location': url_for('get_post', post_id=post.id, _external=True)}
    )


@app.route('/post/<int:post_id>/like', methods=['POST'])
def new_like(post_id):
    post = Post.query.get(post_id)
    if not post:
        return NotFound()

    post.likes += 1
    db.session.add(post)
    try:
        db.session.commit()
    except:
        db.session.rollback()
        raise

    return jsonify(alchemy_object_to_dict(post))

