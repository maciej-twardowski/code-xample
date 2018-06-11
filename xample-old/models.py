from datetime import datetime
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import UserMixin
from xample import db, login_manager


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    posts = db.relationship('Post', backref='author', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Technology(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), index=True, unique=True)

    def __repr__(self):
        return '<Technology {}>'.format(self.name)


class Difficulty(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)

    def __repr__(self):
        return '<Difficulty {}>'.format(self.name)


class Post(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created = db.Column(db.DateTime, index=True, default=datetime.utcnow, nullable=False)
    likes = db.Column(db.Integer, default=0, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    body = db.Column(db.String(250), nullable=False)
    link = db.Column(db.String(200), nullable=False)
    technology = db.Column(db.Integer, db.ForeignKey('technology.id'), nullable=False)
    difficulty = db.Column(db.Integer, db.ForeignKey('difficulty.id'), nullable=False)
    link_accessible = db.Column(db.Boolean, default=None)
    project_name = db.Column(db.String(100), default=None)
    project_author = db.Column(db.String(100), default=None)

    users = db.relationship(User)

    def __repr__(self):
        return '<Post "{}", author_id {}">'.format(self.title, self.author_id)


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


# @login_manager.user_loader
# def load_user(id):
# return User.query.get(int(id))

def clear_data():
    meta = db.metadata
    for table in reversed(meta.sorted_tables):
        print('Clear table %s' % table)
        db.session.execute(table.delete())
    db.session.commit()


def init_db():
    clear_data()

    if User.query.count() == 0 and \
            Technology.query.count() == 0 and \
            Difficulty.query.count() == 0 and \
            Post.query.count() == 0:
        # ~~~~~~~~~~ Users

        admin = User(username='admin')
        admin.set_password('admin')
        guest = User(username='guest')
        guest.set_password('guest')
        test = User(username='test')
        test.set_password('test')

        db.session.add_all([admin, guest, test])
        db.session.commit()

        # ~~~~~~~~~~ Techns

        python = Technology(name='Python')
        cpp = Technology(name='C++')
        java = Technology(name='Java')

        db.session.add_all([python, cpp, java])
        db.session.commit()

        # ~~~~~~~~~~ Difficulites

        easy = Difficulty(name='easy')
        medium = Difficulty(name='medium')
        hard = Difficulty(name='hard')

        db.session.add_all([easy, medium, hard])
        db.session.commit()

        # ~~~~~~~~~~ Posts

        initial_posts = [
            # python
            Post(author_id=admin.id, title='xample',
                 body='distributed web app assignment',
                 link='maciej-twardowski/code-xample',
                 technology=python.id, difficulty=easy.id
                 ),
            Post(author_id=admin.id, title='flask',
                 body='micro web framework',
                 link='pallets/flask',
                 technology=python.id, difficulty=easy.id
                 ),
            Post(author_id=admin.id, title='flask debug toolbar',
                 body='flask debug toolbar extension',
                 link='mgood/flask-debugtoolbar',
                 technology=python.id, difficulty=easy.id
                 ),
            Post(author_id=admin.id, title='scikit',
                 body='python ml library',
                 link='scikit-learn/scikit-learn',
                 technology=python.id, difficulty=easy.id
                 ),
            # cpp
            Post(author_id=guest.id, title='bitcoin',
                 body='Bitcoin Core integration/staging tree',
                 link='bitcoin/bitcoin',
                 technology=cpp.id, difficulty=medium.id
                 ),
            Post(author_id=guest.id, title='pytorch',
                 body='Tensors and Dynamic neural networks',
                 link='pytorch/pytorch',
                 technology=cpp.id, difficulty=medium.id
                 ),
            # java
            Post(author_id=test.id, title='elastic search',
                 body='RESTful Search Engine',
                 link='scikit-learn/scikit-learn',
                 technology=java.id, difficulty=hard.id
                 ),
            Post(author_id=test.id, title='guava',
                 body='Google core libs for Java',
                 link='google/guava',
                 technology=java.id, difficulty=hard.id
                 ),
        ]

        db.session.add_all(initial_posts)
        db.session.commit()
