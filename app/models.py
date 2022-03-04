from enum import unique
from app import app, db
import os
from flask_login import UserMixin


class User(UserMixin, db.Model):
    """
    user who will login to web app and create contacts
    """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(256), unique=True)
    password = db.Column(db.String(256))
    email = db.Column(db.String(256), unique=True)
    name = db.Column(db.String(256))
    password = db.Column(db.String(256))
    contacts =  db.relationship('Contact', backref='user', cascade="all, delete-orphan",  lazy=True)





class Contact(db.Model):
    """
    contacts owned by each user
    Each contact will have name, and a list of phone numbers
    Uniqueness will be measured using checking if a user exists, then if each of the numbers exist for that name


    """
    __tablename__ = 'contact'
    

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(256), unique=False)
    last_name = db.Column(db.String(256), unique=False)
    phone_number = db.Column(db.String(256), unique=True, nullable=True)
    email = db.Column(db.String(256), unique=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    country = db.Column(db.String(256))
    city = db.Column(db.String(256))
    district = db.Column(db.String(256), nullable=True)
    address_line = db.Column(db.String(300))







