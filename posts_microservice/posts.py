#!flask/bin/python
# Based on https://blog.miguelgrinberg.com/post/restful-authentication-with-flask
import json
import os

import pika
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from models import db, Technology, Difficulty, Post


# initialization
app = Flask(__name__)
app.config['SECRET_KEY'] = 'yet another very secret key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts_db.sqlite'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True


def alchemy_object_to_dict(obj):
    return dict((col, getattr(obj, col)) for col in obj.__table__.columns.keys())


@app.route('/', methods=['GET'])
def api_info():
    return jsonify(
        api_requests=[
            '(method | route | arguments)',
            'GET  | /posts | technology, difficulty',
            'GET  | /post/id | ---',
            'GET  | /technologies | ---',
            'GET  | /technology/id | ---',
            'GET  | /difficulties | ---',
            'GET  | /difficulty/id | ---',
            'POST | /post  | author_id, title, body, link, technology, difficulty',
            'POST | /post/id/like | ---',
        ]
    )


@app.route('/posts', methods=['GET'])
def get_posts():
    technology = request.args.get('tech')
    if technology and Technology.query.filter(Technology.id == technology).first() is None:
        return jsonify(succeded=False, error='Technology not found'), 400

    difficulty = request.args.get('diff')
    if difficulty and Difficulty.query.filter(Difficulty.id == difficulty).first() is None:
        return jsonify(succeded=False, error='Difficulty not found'), 400

    filtered_posts = (
        Post.query
            .filter((Post.technology == technology) | (technology == '') | (technology is None))
            .filter((Post.difficulty == difficulty) | (difficulty == '') | (difficulty is None))
            .all()
    )
    post_dicts = [alchemy_object_to_dict(post) for post in filtered_posts]

    return jsonify(post_dicts)


@app.route('/post/<int:id>', methods=['GET'])
def get_post(id):
    post = Post.query.get(id)
    if not post:
        return jsonify(succeded=False, error='Post not found.')

    return jsonify(alchemy_object_to_dict(post))


@app.route('/technologies', methods=['GET'])
def get_technologies():
    technologies_info = [alchemy_object_to_dict(technology) for technology in Technology.query.all()]
    return jsonify(technologies_info)


@app.route('/technology/<int:id>', methods=['GET'])
def get_technology(id):
    technology = Technology.query.get(id)
    if not technology:
        return jsonify(succeded=False, error='Technology not found.')

    return jsonify(alchemy_object_to_dict(technology))


@app.route('/difficulties', methods=['GET'])
def get_difficulties():
    difficulties_info = [alchemy_object_to_dict(difficulty) for difficulty in Difficulty.query.all()]
    return jsonify(difficulties_info)


@app.route('/difficulty/<int:id>', methods=['GET'])
def get_difficulty(id):
    difficulty = Difficulty.query.get(id)
    if not difficulty:
        return jsonify(succeded=False, error='Difficulty not found.')

    return jsonify(alchemy_object_to_dict(difficulty))


def send_to_validation_queue(message):
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='urlValidationQueue')

    channel.basic_publish(exchange='',
                          routing_key='urlValidationQueue',
                          body=message)


@app.route('/post', methods=['POST'])
def new_post():
    author_id = request.json.get('author_id')
    title = request.json.get('title')
    body = request.json.get('body')
    link = request.json.get('link')
    technology = request.json.get('technology')
    difficulty = request.json.get('difficulty')

    if not all(var is not None for var in [author_id, title, body, link, technology, difficulty]):
        return jsonify(succeded=False, error='Missing parameters'), 400

    if Technology.query.filter(Technology.id == technology).first() is None:
        return jsonify(succeded=False, error='Technology not found'), 400

    if Difficulty.query.filter(Difficulty.id == difficulty).first() is None:
        return jsonify(succeded=False, error='Difficulty not found'), 400

    split_link = link.split('/')
    if len(split_link) < 2:
        return jsonify(succeded=False, error='Could not parse project author and/or project name')

    post = Post(author_id=author_id, title=title,
                body=body, link=link, technology=technology,
                difficulty=difficulty, project_name=split_link[1], project_author=split_link[0])

    db.session.add(post)
    db.session.commit()
    send_to_validation_queue(json.dumps({"url": link, "id": post.id}))

    return jsonify(alchemy_object_to_dict(post))


@app.route('/post/<int:id>/update', methods=['POST'])
def update_post_accessibility(id):
    link_accessible = request.json.get('link_accessible')

    if not Post.query.get(id):
        return jsonify(succeded=False, error='Post not found.')

    if link_accessible is None:
        return jsonify(succeded=False, error='Missing parameters'), 400

    post = Post.query.get(id)
    post.link_accessible = link_accessible
    db.session.commit()

    return jsonify(alchemy_object_to_dict(post))


@app.route('/post/<int:id>/rate', methods=['POST'])
def new_like(id):
    post = Post.query.get(id)
    if not post:
        jsonify(succeded=False, error='Post not found.')

    post.likes += 1
    db.session.commit()

    return jsonify(alchemy_object_to_dict(post))


def init_db():
    if not os.path.exists('posts_db.sqlite'):
        db.create_all()

    if Technology.query.count() == 0:
        technologies = [
            Technology(name='Python'),
            Technology(name='C++'),
            Technology(name='Java')
        ]

        for technology in technologies:
            db.session.add(technology)

        try:
            db.session.commit()
        except:
            db.session.rollback()
            raise

    if Difficulty.query.count() == 0:
        difficulties = [
            Difficulty(name='easy'),
            Difficulty(name='medium'),
            Difficulty(name='hard')
        ]

        for difficulty in difficulties:
            db.session.add(difficulty)

        try:
            db.session.commit()
        except:
            db.session.rollback()
            raise


if __name__ == '__main__':
    with app.app_context():
        db.init_app(app)
        init_db()
        app.run(port=5002, debug=True)
