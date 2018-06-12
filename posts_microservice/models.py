import os
from datetime import datetime
from posts_microservice import db
from sqlalchemy import orm


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
    author_name = db.Column(db.String(128), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    body = db.Column(db.String(500), nullable=False)
    link = db.Column(db.String(200), nullable=False)
    technology = db.Column(db.Integer, db.ForeignKey('technology.id'), nullable=False)
    difficulty = db.Column(db.Integer, db.ForeignKey('difficulty.id'), nullable=False)
    link_accessible = db.Column(db.Boolean, default=None)
    project_name = db.Column(db.String(200), default=None)
    project_author = db.Column(db.String(200), default=None)

    @orm.reconstructor
    def init_on_load(self):
        split_link = self.link.split('/')
        if len(split_link) >= 2:
            self.project_author = split_link[0]
            self.project_name = split_link[1]

    def __repr__(self):
        return '<Post "{}", author_name {}">'.format(self.title, self.author_name)


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

    if Post.query.count() == 0:
        initial_posts = [
            # ~~~~ python
            Post(author_name='admin', title='xample',
                 body='distributed web app assignment',
                 link='maciej-twardowski/code-xample',
                 technology=1, difficulty=1
                 ),
            Post(author_name='admin', title='flask',
                 body='micro web framework',
                 link='pallets/flask',
                 technology=1, difficulty=1
                 ),
            Post(author_name='admin', title='flask debug toolbar',
                 body='flask debug toolbar extension',
                 link='mgood/flask-debugtoolbar',
                 technology=1, difficulty=1
                 ),
            Post(author_name='admin', title='scikit',
                 body='python ml library',
                 link='scikit-learn/scikit-learn',
                 technology=1, difficulty=1
                 ),
            # ~~~~ cpp
            Post(author_name='test', title='bitcoin',
                 body='Bitcoin Core integration/staging tree',
                 link='bitcoin/bitcoin',
                 technology=2, difficulty=2
                 ),
            Post(author_name='test', title='pytorch',
                 body='Tensors and Dynamic neural networks',
                 link='pytorch/pytorch',
                 technology=2, difficulty=2
                 ),
            # ~~~~~ java
            Post(author_name='guest', title='elastic search',
                 body='RESTful Search Engine',
                 link='scikit-learn/scikit-learn',
                 technology=3, difficulty=3
                 ),
            Post(author_name='guest', title='guava',
                 body='Google core libs for Java',
                 link='google/guava',
                 technology=3, difficulty=3
                 ),
        ]

        db.session.add_all(initial_posts)
        try:
            db.session.commit()
        except:
            db.session.rollback()
            raise
