
from flask import redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user
from app import db, getApp, login_manager, bcrypt
from app.forms import ContactForm, LoginUser, UserForm
from app.models import Contact, User

app = getApp()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form=UserForm(request.form)
    if request.method == 'POST' and form.validate():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        found = User.query.filter_by(username=form.username.data)
        if found:
            return redirect(url_for('login'))
        else:
            user = User(username=form.username.data,   email=form.email.data, name=form.name.data, password=hashed_password)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('login'))
    return render_template('signup.html', form=form)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/contacts', methods=['GET', 'POST'])
@login_required
def add_contact():
    form = ContactForm(request.form)
    if request.method == 'POST':       
        name = request.form.get('first_name') 
        user = Contact.query.filter_by(first_name=name, last_name=request.form.get('last_name'), owner_id=current_user.id).first()
        if user:
            user_check = Contact(first_name=form.first_name.data, 
            last_name=form.last_name.data, email=form.email.data, 
            phone_number=form.phone.data, owner_id=current_user.id, country=form.country.data, 
            city=form.city.data, district=form.district.data, address_line=form.address_line.data)
            db.session.commit()
        else:
            new_contact = Contact(first_name=form.first_name.data, 
            last_name=form.last_name.data, email=form.email.data, 
            phone_number=form.phone.data, owner_id=current_user.id, country=form.country.data, 
            city=form.city.data, district=form.district.data, address_line=form.address_line.data)
    
            db.session.add(new_contact)  
            db.session.commit
            return redirect(url_for('contacts'))
    return render_template('contacts.html', form=form)

@app.route('/contacts')
@login_required
def contacts():
    contacts = Contact.query.filter_by(owner_id=current_user.id)
    return render_template('contacts.html', contacts=contacts)

@app.route('/delete_contact/<contact_id>', methods=['DELETE'])
def delete_contact(id):
    contact = Contact.query.filter_by(id=id).first()
    if contact:
        db.session.delete(contact)
        db.session.commit()
    else:
        return redirect(url_for('contacts')), "failed to delete contact"


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginUser(request.form)
    if request.method == 'POST':       
        username = request.form.get('username')
        user = User.query.filter_by(username=username).first()
        if user:
            if bcrypt.check_password_hash(user.password, request.form['password']):
                login_user(user)
                return redirect(url_for('contacts'))
            else:
                return redirect(url_for('index')), "FAiled"
        else:
            return redirect(url_for('signup'))
    return render_template('login.html', form=form)



@app.route('/logout')
@login_required
def logout():
   logout_user()
   return redirect(url_for('index'))

@app.route('/profile')
@login_required
def account():
    return render_template("profile.html", user=User.query.filter_by(id=current_user.id).first())

    
@app.route('/update_profile', methods=['GET', 'POST'])
@login_required
def update():
    user = User.query.get(current_user.id)
    form = UserForm(request.form)
    if request.method == 'POST':
        user.name = form.name.data
        user.email = form.email.data
        user.username = form.username.data        
        db.session.commit()
        return redirect(url_for('account'))
    return render_template('edit_profile.html', form=form, user=user)


@app.route('/delete_account')
@login_required
def delete_account():
    User = User.query.filter_by(id=current_user.id).first()
    user  = User.query.filter_by(id=current_user.id).first()
    if User:
        db.session.delete(User), db.session.delete(user)
        db.session.commit()
    db.session.delete(user)
    db.session.commit()
    logout_user()
    return redirect(url_for('index'))