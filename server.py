# -*- coding: utf-8 -*-

from flask import Flask, render_template, request, jsonify, session
from flask_assets import Environment
from jinja2 import StrictUndefined
from datetime import datetime

from model import connect_to_db, db

app = Flask(__name__)

assets = Environment(app)

app.jinja_env.undefined = StrictUndefined
assets.url = app.static_url_path
app.config["ASSETS_DEBUG"] = True
app.secret_key = "abz" 


# Basic Routes *********************************

@app.route("/")
def index_page():
    """Show index page."""

    return render_template("index.html")

@app.route("/new-self-check"):
def add_new_self_check():
    """Add new self check."""

    #TODO: grab form data
    # add instance to self check table

    return redirect("/")


if __name__ == "__main__":

    connect_to_db(app)

    app.run(host="0.0.0.0", port=8000, debug=True)
