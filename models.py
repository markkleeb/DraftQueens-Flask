from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask.ext.wtf import Form

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test2.db'
db = SQLAlchemy(app)


queens = db.Table('queens', 
	db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
	db.Column('queen_id', db.Integer, db.ForeignKey('queen.id')))

class User(db.Model):

	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(80))
	password = db.Column(db.String(80))
	email = db.Column(db.String(120))
	group = db.Column(db.Integer)
	points = db.Column(db.Integer)
	queens = db.relationship('Queen', secondary=queens, backref=db.backref('owners', lazy='dynamic'))
	#queen2 = db.relationship('Queen', backref=db.backref('owners', lazy='dynamic'))
	#queen3 = db.relationship('Queen', backref=db.backref('owners', lazy='dynamic'))

	def __init__(self, username, password, email, group, points):
		self.username = username
		self.password = password
		self.email = email
		self.group = group
		self.points = points
        
        

	def __repr__(self):
		return '<User %r>' % self.username


class Queen(db.Model):

	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(120))
	img = db.Column(db.Text)
	description = db.Column(db.Text)
	active = db.Column(db.Boolean)
	drafted = db.Column(db.Boolean)
	kickedoff = db.Column(db.Boolean)
	points = db.Column(db.Integer)

	def __init__(self, name, img, description, active, points, drafted, kickedoff):
		self.name = name
		self.img = img
		self.description = description
		self.active = active
		self.points = points
		self.drafted = drafted
		self.kickedoff = kickedoff
        
	def __repr__(self):
		return '<User %r>' % self.name



