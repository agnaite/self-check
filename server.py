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
    
    self_checks = QuestionDefinitionSet.query.filter_by(active=True).all()
    
    return render_template("self_checks.html",
                           self_checks=self_checks)

@app.route("/new-self-check")
def add_new_self_check():
    """Add new self check."""

    #TODO: grab form data
    # add instance to self check table

    return render_template("/new_self_check.html")

@app.route("/submit-self-check", methods=["POST"])
def submit_new_self_check():
    """Submit new self-check."""
    
    name = request.form.get("name")

    self_check = QuestionDefinitionSet(name=name, active=True)
    db.session.add(self_check)
    db.session.commit()

    return redirect("/self-checks")


if __name__ == "__main__":

    connect_to_db(app)
    app.run(host="0.0.0.0", port=5002, debug=True)
