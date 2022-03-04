from app import app, db

app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://millicent:Lethabo2016.@localhost/address_book"
if __name__ == '__main__':
    app.run()
    db.create_all()