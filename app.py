import os
from flask import Flask, render_template, redirect, abort, request
from flask.ext.pymongo import PyMongo

import models
from models import User, Queen, db
from flask.ext.sqlalchemy import SQLAlchemy
from flask_googlelogin import GoogleLogin
from flask_oauth import OAuth

DEBUG = True
SECRET_KEY = 'development key'


app = Flask(__name__)
app.debug = DEBUG
app.secret_key = SECRET_KEY
oauth = OAuth()

#Configure SQLAlchemy Database
db.create_all()
#mongo = PyMongo(app)



#Index Page (not yet set up)
@app.route('/')
def index():
   users = User.query.all()
   queens = Queen.query.order_by(Queen.name)

   templateData= {
   'users' : users,
   'queens' : queens
   }
   return render_template("index.html", **templateData)
 

 

#Form to add new users and queens
@app.route('/adduser')
def adduser():
	users = User.query.all()
	queens = Queen.query.all()

	
	
	templateData = {
		'users' : users,
		'queens':queens
		
	}

	return render_template("adduser.html", **templateData)


#Post new User data
@app.route('/newuser', methods=['POST'])
def newuser():
	u = request.form.get('username')
	p = request.form.get('password')
	e = request.form.get('email')
	g = request.form.get('group')
	
	new = User(u, p, e, g, 0)
	db.session.add(new)
	db.session.commit()

	users = User.query.all()
	queens = Queen.query.all()

	templateData = {
		'users': users,
		'queens': queens,
	}

	return render_template("adduser.html", **templateData)


#Post new Queen data
@app.route('/newqueen', methods=['POST'])
def newqueen():
	n = request.form.get('name')
	d = request.form.get('description')
	i = request.form.get('img')
	
	new = Queen(n, i, d, 1, 0, 0, 0)
	db.session.add(new)
	db.session.commit()

	users = User.query.all()
	queens = Queen.query.all()

	templateData= { 'users':users,
	'queens' : queens

	}
	return render_template("adduser.html", **templateData)


#Clear all users
@app.route('/clearall')
def clearall():

 	users = User.query.all()

 	for u in users:
 		db.session.delete(u)
 		db.session.commit()

	return redirect('/')



#Clear specific User
@app.route('/clear/<id>')
def clearone(id):

	
	user = User.query.filter_by(id=id).first()
	db.session.delete(user)
	db.session.commit()


	return redirect('/')
 
 
def main():
    app.run()
 
 
if __name__ == '__main__':
    main()
