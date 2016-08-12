from flask.ext.wtf import Form
from wtforms.fields import StringField, SubmitField



class User(Form):

	username = StringField(u'Name')
	password = StringField(u'Password')
	email = StringField



