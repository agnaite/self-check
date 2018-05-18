# -*- coding: utf-8 -*-

from flask_sqlalchemy import SQLAlchemy
import json

db = SQLAlchemy()


class SelfCheckSession(db.Model):
    """A Self-Check."""

    __tablename__ = "self_check_sessions"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    timestamp = db.Column(db.DateTime())

    answers = db.relationship("Answer", backref="self_check_session")


class QuestionDefinitionSet(db.Model):
    """A set of questions."""

    __tablename__ = "question_definition_sets"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(64), nullable=False, unique=True)
    active = db.Column(db.Boolean, default=True)

class QuestionDefinition(db.Model):
    """A Question."""

    __tablename__ = "question_definitions"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    question_definition_set_id = db.Column(db.ForeignKey("question_definition_sets.id"))
    body = db.Column(db.Text, nullable=False)
    response_type_id = db.Column(db.String(3), nullable=False)

    question_definition_set = db.relationship("QuestionDefinitionSet", backref="question_definitions")


class Answer(db.Model):
    """An Answer."""

    __tablename__ = "answers"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    self_check_session_id = db.Column(db.ForeignKey("self_check_sessions.id"))
    question_definition_id = db.Column(db.Integer, db.ForeignKey("question_definitions.id"))
    response = db.Column(db.String(240), nullable=False)
    
    question_definition = db.relationship("QuestionDefinition", backref="answers")

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
