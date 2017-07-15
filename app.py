# -*- coding: utf-8 -*-
"""
Created on Sat Jul 15 12:38:38 2017

@author: iansp
"""

import flask
from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello():
    return flask.render_template('splash.html')

@app.route("/vvhen")
def vvhen():
    return flask.render_template('planner_name.html')

@app.route('/submit-planner-info', methods=['POST'])
def new_user():
    error = None
    name = flask.request.form['plannername']
    email = flask.request.form['email']

    if user and email is None:
        error = "Fields can't be blank"
        return flask.render_template('planner_name.html', error=error)

    return flask.render_template('planner_name.html')