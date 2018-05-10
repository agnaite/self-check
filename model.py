# -*- coding: utf-8 -*-

from flask_sqlalchemy import SQLAlchemy
import json

db = SQLAlchemy()


class SelfCheck(db.Model):
    """A Self-Check."""

    __tablename__ = "self_checks"

    self_check_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(64), nullable=False, unique=True)
    created_at = db.Column(db.DateTime())
    archived = db.Column(db.Boolean, default=False)

    questions = db.relationship("Question", secondary="self_check_questions", backref="self_checks")

class Question(db.Model):
    """A Question."""

    __tablename__ = "questions"

    question_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    question = db.Column(db.Text, nullable=False)
    response_type_id = db.Column(db.String(3), nullable=False)

    answers = db.relationship("Answer", backref="questions")
    

class SelfCheckQuestion(db.Model):
    """A Self-Check Question."""

    __tablename__ = "self_check_questions"

    self_check_question_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    self_check_id = db.Column(db.Integer, db.ForeignKey("self_checks.self_check_id"))
    question_id = db.Column(db.Integer, db.ForeignKey("questions.question_id"))


class Answer(db.Model):
    """An Answer."""

    __tablename__ = "answers"

    answer_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    question_id = db.Column(db.Integer, db.ForeignKey("questions.question_id"))
    answer = db.Column(db.String(240), nullable=False)
    timestamp = db.Column(db.DateTime())


def connect_to_db(app):
    """Connect the database to the Flask app."""

    # Configure to use our database
    app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///selfchecks"

    app.config["SQLALCHEMY_ECHO"] = True
    db.app = app
    db.init_app(app)


if __name__ == "__main__":

    from server import app

    connect_to_db(app)
    db.create_all()
 
    print("Connected to DB.")
