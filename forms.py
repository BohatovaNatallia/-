from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
	loginField = StringField('loginField', validators=[DataRequired()])
	passwordField = StringField('passwordField', validators=[DataRequired()])


class RegisterForm(FlaskForm):
	loginField = StringField('loginField', validators=[DataRequired()])
	passwordField = StringField('passwordField', validators=[DataRequired()])


class UserDataForm(FlaskForm):
	nameField = StringField('nameField', validators=[DataRequired()])
	surnameField = StringField('surnameField', validators=[DataRequired()])
	lastnameField = StringField('lastnameField', validators=[DataRequired()])
