from distutils.debug import DEBUG
import os
import secrets
from flask import Flask, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt


app = Flask(__name__)



db = SQLAlchemy(app)
db.init_app(app)
secret_key = secrets.token_urlsafe(16)
app.config['SECRET_KEY'] = secret_key
app.config.setdefault('SQLALCHEMY_DATABASE_URI', "mysql+pymysql://millicent:Lethabo2016.@localhost/address_book")
app.config['SQLALCHEMLY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
db.init_app(app)
with app.app_context():
    db.create_all()




bcrypt = Bcrypt(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = "Login to Continue"





# def getApp():
#     return app

# from app import routes


if __name__ =='__main__':
    app.run(debug=True)