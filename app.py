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
   users = User.query.order_by(User.group).order_by(User.points)
   queens = Queen.query.order_by(Queen.name)

   templateData= {
   'users' : users,
   'queens' : queens
   }
   return render_template("index.html", **templateData)
 

@app.route('/queens')
def queens():

	queens = Queen.query.order_by(Queen.name)

	templateData = {
	'queens' : queens
	}

	return render_template("queens.html", **templateData)


@app.route('/admin')
def editpoints():

	users = User.query.order_by(User.group).order_by(User.points)


	templateData = {

	'users' : users,

	}

	return render_template("editpoints.html", **templateData)

@app.route('/changepoints/<id>', methods=['POST'])
def changepoints(id):

	user = User.query.filter_by(id=id).first()

	points = request.form.get('points')

	user.points = points

	return redirect('/')



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

#Add Owner to Queen
@app.route('/addowner/<id>', methods=['GET', 'POST'])
def addowner(id):

	
	queen = Queen.query.filter_by(id=id).first()
	queen.drafted = True

	user = User.query.filter_by(username=request.form.get('owner')).first()

	user.queens.append(queen)
	
	return redirect('/queens')


#Remove Owner
@app.route('/clearowner/<id>', methods=['GET', 'POST'])
def removeowner(id):
	queen = Queen.query.filter_by(id=id).first()
	queen.drafted = False

	queen.owners = ''

	return redirect('/queens')


#CLONE A QUEEN
@app.route('/duplicate/<id>')
def duplicate(id):
	
	
	queen = Queen.query.filter_by(id=id).first()

	

	n = queen.name
	d = queen.description
	i = queen.img
	k = queen.kickedoff
	p = queen.points

	new = Queen(n, i, d, 0, p, 0, k)
	db.session.add(new)
	db.session.commit()

	return redirect('/queens')





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


	return redirect('/adduser')

#Delete Queen
@app.route('/delete/<id>')
def deleteone(id):

	
	queen = Queen.query.filter_by(id=id).first()
	db.session.delete(queen)
	db.session.commit()


	return redirect('/queens')
 
 
def main():
    app.run()
 
 
if __name__ == '__main__':
    main()
