from email.policy import default
from enum import unique
from genericpath import exists
from tabnanny import check
from urllib import response
from flask import Flask, request, jsonify, Response, make_response
from flask_sqlalchemy import SQLAlchemy
from requests import session
from sqlalchemy.orm import backref, relationship, declarative_base
from sqlalchemy.sql import func
from sqlalchemy import Column, Integer, DateTime
import base64
import json
from datetime import datetime
import os

app = Flask(__name__)
Base = declarative_base()

app.config['SQLALCHEMY_DATABASE_URI'] ='mysql://newuser:password@localhost/new'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class user(db.Model):
    userid = db.Column(db.Integer, primary_key=True)
    username= db.Column(db.String(100))
    password = db.Column(db.String(80),unique=True)
    fname= db.Column(db.String(80))
    lname= db.Column(db.String(80))
    email = db.Column(db.String(80),unique=True)
    created_at = db.Column(DateTime(timezone=True), server_default=func.now())
    updated_at = db.Column(DateTime(timezone=True), onupdate=func.now())
    #session = db.relationship("session", backref="user", lazy='dynamic')

def __init__(self, username, password,fname, lname, email):
    self.username=username
    self.password=password
    self.fname=fname
    self.lname=lname
    self.email=email

class Session(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.Integer, db.ForeignKey('user.userid'))
    #user = db.relationship("user", back_populates="session" )
    user = db.relationship("user", backref=backref("user", uselist=False))
    session_token = db.Column(db.String(80),unique=True)
    status = db.Column(db.Integer, default=1)
    
    def __init__(self,userid,session_token,status):
        self.userid=userid
        self.session_token=session_token
        self.status=status

def get_token(userid):
    now = datetime.now()
    timestamp = datetime.timestamp(now)
    s = (str(userid)+str(timestamp))
    s = s.encode('ascii')
    session_token = base64.b64encode(s)
    session_token = str(session_token)
    return session_token
    
#db.drop_all()
db.create_all()

@app.route("/signup", methods=["POST"])
def signup():
    data = request.json
    username = data['username']
    password = data['password']
    query = user.query.filter_by (username=username).first()
    if query:
        return jsonify({'message': 'user already exists'})
    else:
        new_user = user(username = data['username'], password = data['password'], fname = data['fname'], lname = data['lname'], email = data['email'])
        db.session.add(new_user)
        db.session.commit()
        message = json.dumps({"message":"new user {} created".format(data["username"])})
    return Response(message,status=201)


@app.route("/login", methods=["POST"])
def login():
    data = request.json
    username = data['username']
    password = data['password']
    user_query = user.query.filter_by(username = username).first()
    user_pass = user.query.filter_by(password = password).first()
    if user_query and user_pass:
        #now = datetime.now()
        #timestamp = datetime.timestamp(now)
        userid = user_query.userid
        token = get_token(userid)
        new_session = Session(userid,token,1)
        db.session.add(new_session)
        db.session.commit()
        message = "login"
    else:
        message = "you are not found.....please signup"

    #message = json.dumps({"message":" {} logot".format(data["username"])})
    #return Response(message, status=201)
    return Response (message)

@app.route("/logout/<u_id>", methods=["GET"])
def logout(u_id):
    session_token = get_token(u_id)
    query = Session.query.filter_by (userid=u_id).first()
    if query:
        query.status = 0
        db.session.commit()
        message = " user logout"
    else:
        message ="user not fount"
    return message


if __name__ =='__main__':
    app.run(debug=True)