from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Technology(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), index=True, unique=True)

    def __repr__(self):
        return '<Technology {}>'.format(self.name)


class Difficulty(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)

    def __repr__(self):
        return '<Difficulty {}>'.format(self.name)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created = db.Column(db.DateTime, index=True, default=datetime.utcnow, nullable=False)
    likes = db.Column(db.Integer, default=0, nullable=False)
    author_id = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String(100), nullable=False)
    body = db.Column(db.String(250), nullable=False)
    link = db.Column(db.String(200), nullable=False)
    technology = db.Column(db.Integer, db.ForeignKey('technology.id'), nullable=False)
    difficulty = db.Column(db.Integer, db.ForeignKey('difficulty.id'), nullable=False)
    link_accessible = db.Column(db.Boolean, default=None)
    project_name = db.Column(db.String(100), default=None)
    project_author = db.Column(db.String(100), default=None)

    def __repr__(self):
        return '<Post "{}", author_id {}">'.format(self.title, self.author_id)


