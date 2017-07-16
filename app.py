# -*- coding: utf-8 -*-
"""
Created on Sat Jul 15 12:38:38 2017

@author: iansp
"""

import flask
from flask import Flask
from flask_mail import Mail
from flask_mail import Message
import smtplib

app = Flask(__name__)
app.config.from_object(__name__)

app.config.update(dict(
    DEBUG = True,
    MAIL_SERVER = 'smtp.gmail.com',
    MAIL_PORT = 587,
    MAIL_USE_TLS = True,
    MAIL_USE_SSL = False,
    MAIL_USERNAME = 'monkeysupremacy@gmail.com',
    MAIL_SUPPRESS_SEND = False
))

mail = Mail(app)

@app.route("/")
def hello():
	return flask.render_template('splash.html')

@app.route("/vvhen")
def vvhen():
	return flask.render_template('planner_name.html')

@app.route('/submit-planner-info', methods=['POST'])
def new_user():
	error = None
	planner_name = flask.request.form['plannername']
	email = flask.request.form['email']

	if planner_name and email is None:
		error = "Fields can't be blank"
		return flask.render_template('planner_name.html', error=error)

	return flask.render_template('planner_information.html', planner_name=planner_name, planner_email=planner_name)

@app.route("/list-of-invitees")
def list_of_invitees():
	return flask.render_template('list_of_invitees.html')

@app.route('/send-invitee-email', methods=['POST'])
def send_invitee_email():


	sender = 'monkeysupremacy@gmail.com'
	receivers = ['monkeysupremacy@gmail.com']

	to = sender
	gmail_user = sender
	smtpserver = smtplib.SMTP("smtp.gmail.com",587)
	smtpserver.ehlo()
	smtpserver.starttls()
	smtpserver.ehlo
	smtpserver.login(gmail_user, gmail_pwd)
	header = 'To:' + to + '\n' + 'From: ' + gmail_user + '\n' + 'Subject:testing \n'
	print header
	msg = header + '\n this is test msg from mkyong.com \n\n'
	smtpserver.sendmail(gmail_user, to, msg)
	print 'done!'
	smtpserver.close()

	msg = Message("Hello",
				  sender="monkeysupremacy@gmail.com", # from
				  recipients=["monkeysupremacy@gmail.com"]) # to
	msg.body = "testing"
	mail.send(msg)

	return flask.render_template('thanks_invitee.html')

	invitee_name = flask.request.form['inviteename']
	invitee_email = flask.request.form['inviteeemail']

	if inviteename and inviteeemail is None:
		error = "Fields can't be blank"
		return flask.render_template('list_of_invitees.html', error=error)


	return flask.render_template('thanks_invitee.html', invitee_name=invitee_name, invitee_email=invitee_email)

