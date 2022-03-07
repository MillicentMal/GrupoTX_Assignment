from email import message
from hashlib import new
from lib2to3.pgen2 import token
from uuid import uuid4
from flask import Flask, abort
from flask import render_template, request
from flask.helpers import flash, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import null
from werkzeug.utils import redirect
from flask_wtf import Form
from wtforms import StringField, PasswordField, validators
from wtforms.fields.numeric import IntegerField
from wtforms.fields.simple import EmailField, SubmitField, FileField

# app creation adn configuration
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///storage.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = "secret_key"
db = SQLAlchemy(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add_contact', methods=['GET', 'POST'])
def add_contact():
    form = ContactForm(request.form)
    if request.method == 'POST':       
        new_contact = Contact(token=str(uuid4()), first_name=form.first_name.data, 
            last_name=form.last_name.data, email=form.email.data, 
            phone_number=form.phone.data, country=form.country.data, 
            city=form.city.data, district=form.district.data, address_line=form.address_line.data)
        contact = Contact.query.filter_by(first_name=new_contact.first_name, last_name=new_contact.last_name).first()
        if contact:
            if contact.phone_number is not None and contact.phone_number == form.phone.data:
                return redirect(url_for('edit_contact'))                   
            else:
                try:
                    db.session.add(new_contact)
                    db.session.commit()
                except:
                    abort(403)
                  
        else:
            db.session.add(new_contact)  
            db.session.commit()
            token = new_contact.token
            return render_template('token.html', token=token)
    return render_template('add_contact.html', form=form)

       

@app.route('/edit_contact/<int:id>', methods=['GET', 'POST'])
def edit_contact(id):
    contact = Contact.query.filter_by(id=id).first() 
    form = EditForm(request.form)
    if request.method == 'POST':
        
        if contact:
            contact.token = form.token.data
            contact.first_name = form.first_name.data
            contact.last_name = form.last_name.data  
            contact.email= form.email.data
            contact.phone_number = form.phone.data 
            contact.country = form.country.data
            contact.city = form.city.data
            contact.district = form.district.data
            contact.address_line = form.address_line.data
            try:
                db.session.commit()
            except:
                abort(403)
            return redirect(url_for('contacts'))   
        else:
            return redirect(url_for('contacts'))    
    return render_template('edit_contact.html', form=form, contact=contact)

@app.route('/contacts')
def contacts():
    """
    displays all contacts
    """
    search = request.args.get('search')
    if search:
        contacts = Contact.query.filter(Contact.first_name.contains(search) | Contact.last_name.contains(search))

    else:
        contacts = Contact.query.all()
    return render_template('contacts.html', contacts=contacts)


@app.route('/delete_contact/<int:id>', methods=['GET', 'POST'])
def delete_contact(id):
    token = request.form.get('token')
    contact = Contact.query.filter_by(token=token).first()
    if contact:
        try:
            db.session.delete(contact)
            db.session.commit()
        except:
            abort(404)
        return redirect(url_for('contacts'))
    return render_template('delete_contact.html')

class ContactForm(Form):
    first_name = StringField('FirstName',  validators=[validators.input_required()])
    last_name = StringField('LastName',  validators=[validators.input_required()])
    email = EmailField('Email')
    address_line = StringField('Address')
    city = StringField('City')
    country = StringField('Country')
    district = StringField('District')
    phone = StringField('Phone')
    submit = SubmitField()

class EditForm(Form):
    first_name = StringField('FirstName',  validators=[validators.input_required()])
    last_name = StringField('LastName',  validators=[validators.input_required()])
    email = EmailField('Email')
    address_line = StringField('Address')
    city = StringField('City')
    country = StringField('Country')
    district = StringField('District')
    phone = StringField('Phone')
    token = PasswordField('Token')
    submit = SubmitField()
   


class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(256), unique=False)
    last_name = db.Column(db.String(256), unique=False)
    phone_number = db.Column(db.String(256), nullable=True)
    email = db.Column(db.String(256), nullable=True)
    country = db.Column(db.String(256))
    city = db.Column(db.String(256))
    district = db.Column(db.String(256), nullable=True)
    address_line = db.Column(db.String(300))
    token = db.Column(db.String(256))







if __name__ =="__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)