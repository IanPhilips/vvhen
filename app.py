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