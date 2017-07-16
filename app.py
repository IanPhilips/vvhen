# -*- coding: utf-8 -*-
"""
Created on Sat Jul 15 12:38:38 2017

@author: iansp
"""
import datetime
import uuid
import pycronofy
import os
from flask import Flask,redirect, abort, request, url_for 


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

calendarIDs = []

#global cronofy
example_datetime_string = '2016-01-06T16:49:37Z' #ISO 8601.

# To set to local time, pass in the tzid argument.
from_date = (datetime.datetime.utcnow() - datetime.timedelta(days=2))
to_date = datetime.datetime.utcnow()


@app.route("/authorizeUserCalendar")
def authorizeUserCalendar():
  global cronofy
  cronofy = pycronofy.Client(client_id="BQYkMYzj2xSA8iZUnumgng0-NthBcRZy", client_secret="7ckUqdSRcFHaaWx2LoIWrN_7SyQzcBErRqfV2VJ33T673TOYWu8VUF_WdhPyuHwcFa3Tecqv8ADYyhpeKrtuYQ")
  url = cronofy.user_auth_link('http://palebone.myddns.me/calendar')
  #print('Go to this url in your browser, and paste the code below')
  #print(url)

  #code = input('Paste Code Here: ') # raw_input() for python 2.
  #auth = cronofy.get_authorization_from_code(code)
  #print(auth)
 # site = "https://app.cronofy.com/oauth/authorize?response_type=code&client_id=BQYkMYzj2xSA8iZUnumgng0-NthBcRZy&redirect_uri=http://palebone.myddns.me/calendar&scope=read_events&state=true"
  return redirect(url, code=302)

@app.route("/calendar", methods=['GET'])
def calendar():
    print("1")
    #global cronofy
    #cronofy = pycronofy.Client(client_id="BQYkMYzj2xSA8iZUnumgng0-NthBcRZy", client_secret="7ckUqdSRcFHaaWx2LoIWrN_7SyQzcBErRqfV2VJ33T673TOYWu8VUF_WdhPyuHwcFa3Tecqv8ADYyhpeKrtuYQ")
    print("2")
    code = str(request.args.get('code', None))
    print("3")
    print("code is ", code)
    auth = cronofy.get_authorization_from_code(code)
    print("4")
    global cronofy
    cronofy = pycronofy.Client(client_id="BQYkMYzj2xSA8iZUnumgng0-NthBcRZy", client_secret="7ckUqdSRcFHaaWx2LoIWrN_7SyQzcBErRqfV2VJ33T673TOYWu8VUF_WdhPyuHwcFa3Tecqv8ADYyhpeKrtuYQ", 
    access_token=auth['access_token'],
    refresh_token=auth['refresh_token'],
    token_expiration=auth['token_expiration'])
    calendars = cronofy.list_calendars()    
    for i in range(len(calendars)):
        print("calendar: " + str(calendars[i]["calendar_id"]))
        calendarIDs.append(calendars[i]["calendar_id"])
         
        
#    calendarIDs.append(calendarID)
   # print(calendarID)
    findFreeBlocks()
    if len(calendarIDs)>2:
        return redirect(url_for("CombinedCalendar"), code=302)
    return "you did it!"
    

def findFreeBlocks():
  #cronofy = pycronofy.Client(client_id="BQYkMYzj2xSA8iZUnumgng0-NthBcRZy", client_secret="7ckUqdSRcFHaaWx2LoIWrN_7SyQzcBErRqfV2VJ33T673TOYWu8VUF_WdhPyuHwcFa3Tecqv8ADYyhpeKrtuYQ")
  print( cronofy.is_authorization_expired())
# Refresh
# Refresh requires the client id and client secret be set.
  auth = cronofy.refresh_authorization()
  print(auth)
  print( cronofy.is_authorization_expired())
 # global cronofy
  #cronofy = pycronofy.Client(client_id="BQYkMYzj2xSA8iZUnumgng0-NthBcRZy", client_secret="7ckUqdSRcFHaaWx2LoIWrN_7SyQzcBErRqfV2VJ33T673TOYWu8VUF_WdhPyuHwcFa3Tecqv8ADYyhpeKrtuYQ",
  #access_token=auth['access_token'],
  #refresh_token=auth['refresh_token'],
  #token_expiration=auth['token_expiration'])
  #for calendarID in calendarIDs:
#  print(cronofy.list_calendars())
  free_busy_blocks = cronofy.read_free_busy(calendar_ids=(calendarIDs[0], calendarIDs[1],calendarIDs[2]),
  from_date=from_date,
  to_date=to_date
  )
  print("contacting cronofy for free blocks")
  for block in free_busy_blocks:
    print("block is:")
 
  print(len(calendarIDs))
  if len(calendarIDs)>2:
    return redirect(url_for("CombinedCalendar"), code=302)
 

@app.route("/CombinedCalendar")
def CombinedCalendar():  
#return calendar.html 
  return flask.render_template('invitee_calendar.html')

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


