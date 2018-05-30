# -*- coding: utf-8 -*-

from flask_sqlalchemy import SQLAlchemy
import json

db = SQLAlchemy()


class SelfCheckSession(db.Model):
    """A self-check session."""

    __tablename__ = "self_check_sessions"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    question_definition_set_id = db.Column(db.ForeignKey("question_definition_sets.id"))
    timestamp = db.Column(db.DateTime())
    
    question_definition_sets = db.relationship("QuestionDefinitionSet", backref="self_check_sessions")
    answers = db.relationship("Answer", backref="self_check_sessions")


class QuestionDefinitionSet(db.Model):
    """A set of questions."""

    __tablename__ = "question_definition_sets"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(64), nullable=False, unique=True)
    active = db.Column(db.Boolean, default=True)

class QuestionDefinition(db.Model):
    """A question definition."""

    __tablename__ = "question_definitions"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    question_definition_set_id = db.Column(db.ForeignKey("question_definition_sets.id"))
    body = db.Column(db.Text, nullable=False)

    question_definition_sets = db.relationship("QuestionDefinitionSet", backref="question_definitions")


class Answer(db.Model):
    """An answer to a question."""

    __tablename__ = "answers"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    self_check_session_id = db.Column(db.ForeignKey("self_check_sessions.id"))
    question_definition_id = db.Column(db.ForeignKey("question_definitions.id"))
    response = db.Column(db.String(240), nullable=False)
    
    question_definitions = db.relationship("QuestionDefinition", backref="answers")

def connect_to_db(app):
    """Connect the database to the Flask app."""

    # Configure to use our database
    app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///selfchecks"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
    app.config["SQLALCHEMY_ECHO"] = True 

    db.app = app
    db.init_app(app)


if __name__ == "__main__":

    from server import app

    connect_to_db(app)
    db.drop_all()
    db.create_all()
 
    print("Connected to DB.")
