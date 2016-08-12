import os
from flask import Flask, render_template, redirect, abort
from flask.ext.pymongo import PyMongo

import models
from flask.ext.sqlalchemy import SQLAlchemy
from flask_googlelogin import GoogleLogin


app = Flask(__name__)

#Configure SQLAlchemy Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)
#mongo = PyMongo(app)


#Configure Google Login API
googlelogin = GoogleLogin(app)

from flask_login import LoginManager
login_manager = LoginManager()
login_manager.init_app(app)
googlelogin = GoogleLogin(app, login_manager)



#Index Page
@app.route('/', methods=['GET'])
def index():
	return render_template("index.html")


#Copied from Flask-Google Tutorial
@app.route('/oauth2callback')
@googlelogin.oauth2callback
def create_or_update_user(token, userinfo, **params):
    user = User.filter_by(google_id=userinfo['id']).first()
    if user:
        user.name = userinfo['name']
        user.avatar = userinfo['picture']
    else:
        user = User(google_id=userinfo['id'],
                    name=userinfo['name'],
                    avatar=userinfo['picture'])
    db.session.add(user)
    db.session.flush()
    login_user(user)
    return redirect(url_for('index'))




@app.route('/profile', methods=['GET'])
#@login_required
def profile():
    return render_template("index.html")

