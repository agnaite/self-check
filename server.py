# -*- coding: utf-8 -*-

from flask import Flask, render_template, request, jsonify, session, redirect
from flask_assets import Environment
from jinja2 import StrictUndefined
from datetime import datetime

from model import connect_to_db, db, QuestionDefinition, QuestionDefinitionSet, Answer, SelfCheckSession


app = Flask(__name__)

assets = Environment(app)

app.jinja_env.undefined = StrictUndefined
assets.url = app.static_url_path
app.config["ASSETS_DEBUG"] = True
app.config["ENV"] = "development"
app.secret_key = "abz" 


# Basic Routes *********************************

@app.route("/")
def index_page():
    """Show index page."""
    print("APP CONFIG ", app.config)
    return render_template("index.html")

@app.route("/self-checks")
def show_all_self_checks():
    """Show all active self-checks."""
    
    self_checks = QuestionDefinitionSet.query.all()
    
    return render_template("self_checks.html",
                           self_checks=self_checks)

@app.route("/self-check/<self_check_id>")
def show_self_check(self_check_id):
    """Show single self-check"""

    self_check = QuestionDefinitionSet.query.get(int(self_check_id))
    questions = self_check.question_definitions 
    
    sessions = self_check.self_check_sessions

    return render_template("self_check.html",
                           self_check=self_check,
                           questions=questions,
                           sessions=sessions)

@app.route("/take-self-check/<self_check_id>")
def take_self_check(self_check_id):
    """Take a self-check."""

    self_check = QuestionDefinitionSet.query.get(int(self_check_id))
    questions = self_check.question_definitions

    return render_template("take_self_check.html",
                           self_check=self_check,
                           questions=questions)

@app.route("/submit-self-check/<self_check_id>", methods=["POST"])
def submit_self_check(self_check_id):
    """Submit a self-check"""

    self_check = QuestionDefinitionSet.query.get(int(self_check_id))
    questions = self_check.question_definitions
    
    self_check_session = SelfCheckSession(timestamp=datetime.now(),
                                          question_definition_set_id=int(self_check_id))
    db.session.add(self_check_session)
    db.session.commit()

    for question in questions:
        response = request.form.get(str(question.id))
        answer = Answer(response=response,
                        self_check_session_id=self_check_session.id,
                        question_definition_id=question.id)

        db.session.add(answer)

    db.session.commit()

    return redirect("/self-checks")
    

@app.route("/new-self-check")
def add_new_self_check():
    """Add new self check."""

    return render_template("/new_self_check.html")

@app.route("/submit-self-check", methods=["POST"])
def submit_new_self_check():
    """Submit new self-check."""
    
    name = request.form.get("name")

    self_check = QuestionDefinitionSet(name=name, active=True)
    db.session.add(self_check)
    db.session.commit()

    return redirect("/add-question/"+str(self_check.id))

@app.route("/archive-self-check/<self_check_id>")
def archive_self_check(self_check_id):
    """Archive a self-check."""

    self_check = QuestionDefinitionSet.query.get(int(self_check_id))
    self_check.active = False
    
    questions = self_check.question_definitions

    for question in questions:
        db.session.delete(question)

    db.session.commit()

    return redirect("/self-checks")

@app.route("/add-question/<self_check_id>")
def add_question(self_check_id):
    """Add questiont to self-check."""

    return render_template("add_question.html", 
                           self_check_id=self_check_id)

@app.route("/submit-question", methods=["POST"])
def submit_new_question():
    """Submit new self-check."""
    
    self_check_id = request.form.get("self_check_id")
    question = request.form.get("question")

    question_definition = QuestionDefinition(body=question, 
                                             question_definition_set_id=int(self_check_id))
    db.session.add(question_definition)
    db.session.commit()

    return redirect("/add-question/"+self_check_id)


if __name__ == "__main__":

    connect_to_db(app)
    app.run(host="0.0.0.0", port=5000, debug=True)
