# import os
# from sqlalchemy import create_engine
from flask_sqlalchemy import SQLAlchemy
# import json

database_name = "trivia"
username = "admin"
password = "abc123"
host_port = "localhost:5432"
database_path = "postgres://{}:{}@{}/{}".format(
    username,
    password,
    host_port,
    database_name)

db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''


def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()


'''
Category

'''


class Category(db.Model):
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)

    # same category can not be added twice.
    type = db.Column(db.String(), unique=True)

    # one to many relation with Question
    questions = db.relationship(
        'Question',
        backref='category',
        passive_deletes=True,
        lazy=True)

    def __init__(self, type):
        self.type = type

    def format(self):
        return {
            'id': self.id,
            'type': self.type
        }


'''
Question

'''


class Question(db.Model):
    __tablename__ = 'questions'

    id = db.Column(db.Integer, primary_key=True)

    # same question can not be added twice.
    question = db.Column(db.String(), unique=True)
    answer = db.Column(db.String())
    difficulty = db.Column(db.Integer)
    category_id = db.Column(
        db.Integer,
        db.ForeignKey('categories.id', ondelete='CASCADE'),
        nullable=True)

    def __init__(self, question, answer, category, difficulty):
        self.question = question
        self.answer = answer
        self.category = category
        self.difficulty = difficulty

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    # as per the frontend, we need to return the category id in category
    # and it should be degremented by one to show the right icon
    def format(self):
        return {
            'id': self.id,
            'question': self.question,
            'answer': self.answer,
            'category': self.category.id,
            'difficulty': self.difficulty
        }
