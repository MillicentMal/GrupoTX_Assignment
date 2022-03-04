from tokenize import String
from app.models import Contact
from app import app, db 
from flask_wtf import Form
from wtforms import StringField, PasswordField, validators
from wtforms.fields.numeric import IntegerField
from wtforms.fields.simple import EmailField, SubmitField, FileField

class UserForm(Form):
    name = StringField('Name',  validators=[validators.input_required()])
    email = EmailField('Email',  validators=[validators.input_required(), validators.Length(min=1, max=50)])
    username = StringField('Username',  validators=[validators.input_required(), validators.Length(min=1, max=50)])
    password = PasswordField('Password', validators=[validators.input_required(), validators.Length(min=8, max=50)])
    password_check = PasswordField('Confirm',  validators=[validators.input_required(), validators.Length(min=1, max=50), validators.EqualTo('password',
                             message="Passwords must match")])
    submit = SubmitField("Create Account")


class LoginUser(Form):
    username = StringField('Username',  validators=[validators.input_required(), validators.Length(min=1, max=50)])
    password = PasswordField('Password', validators=[validators.input_required(), validators.Length(min=8, max=50)])
    password_check = PasswordField('Confirm',  validators=[validators.input_required(), validators.Length(min=1, max=50), validators.EqualTo('password',
                             message="Passwords must match")])
    submit = SubmitField("Login Account")



class ContactForm(Form):
    first_name = StringField('FirstName',  validators=[validators.input_required()])
    last_name = StringField('LastName',  validators=[validators.input_required()])
    email = EmailField('Email')
    address_line = StringField('Address')
    city = StringField('City')
    country = StringField('Country')
    district = StringField('District')
    phone = StringField('Phone', default="Enter phone number")
    submit = SubmitField()



