from flask import Flask
from flask import render_template, request
from flask.helpers import flash, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import login_manager, LoginManager, current_user, login_required, login_user, logout_user, UserMixin, user_logged_in
from werkzeug.utils import redirect
from flask_wtf import Form
from wtforms import StringField, PasswordField, validators
from wtforms.fields.numeric import IntegerField
from wtforms.fields.simple import EmailField, SubmitField, FileField

# app creation adn configuration
app = Flask(__name__)
# failing to deploy
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
        name = request.form.get('first_name') 
        user = Contact.query.filter_by(first_name=name, last_name=request.form.get('last_name')).first()
        if user:
            return redirect(url_for('contacts'))
        else:
            new_contact = Contact(first_name=form.first_name.data, 
            last_name=form.last_name.data, email=form.email.data, 
            phone_number=form.phone.data, country=form.country.data, 
            city=form.city.data, district=form.district.data, address_line=form.address_line.data)
            db.session.add(new_contact)  
            db.session.commit()
            return redirect(url_for('contacts'))
    return render_template('add_contact.html', form=form)

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

# @app.route('/delete_contact/<int:contact_id>')
# def delete_contact(contact_id):
#     contact = Contact.query.filter_by(id=contact_id).first()
#     if contact:
#         db.session.delete(contact)
#         db.session.commit()
#     else:
#         return redirect(url_for('contacts')), "failed to delete contact"

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







if __name__ =="__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)