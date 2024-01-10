
#import SQLalchemy extension
#revisit this import

# from flask import Flask

from flask_sqlalchemy import SQLAlchemy


#set a variable to the database object

database= SQLAlchemy()


#connect the database with Flask

#using the skeleton for the connection in the sql-alchemy 1 lecture
#note that there is a slight mod to be similar to the flask-sqlalchemy doc

def database_connect(app,database_name):

    app.config["SQLALCHEMY_DATABASE_URI"] = f"postgresql:///{database_name}"
    app.config["SQLALCHEMY_ECHO"] = True
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    

    database.app = app
    database.init_app(app)


#define the three classes


class Animal(database.Model):


    __tablename__ = "animals"

    #does this need to be a primary key?

    id = database.Column(database.Integer,primary_key=True,autoincrement=True)
    name = database.Column(database.Text, nullable=False)
    type = database.Column(database.Text, nullable=False)
    breed = database.Column(database.Text, nullable=False)
    join_date = database.Column(database.DateTime, nullable=True)
    age = database.Column(database.Integer, nullable=False)
    weight = database.Column(database.Integer, nullable=True)
    gender = database.Column(database.Text, nullable=False)
    #decision to make on if nullable or not
    scheduled_euthanasia_date = database.Column(database.Date, nullable=True)
    adopt_code = database.Column(database.Text, nullable=False)
    bio = database.Column(database.Text, nullable=True)
    entry_source = database.Column(database.Text, nullable=False)
    shelter_id = database.Column(database.Integer, database.ForeignKey('shelters.id'))

    #relationship between animal and shelter

    shelter = database.relationship('Shelter',back_populates="animal")

    #repr for Animal class

    def __repr__(self):
        return f"<id={self.id} name={self.name} type={self.type}>"
    
class User(database.Model):

    __tablename__ = "users"

    #does this need to be a primary key?
    
    id = database.Column(database.Integer,primary_key=True,autoincrement=True)
    username = database.Column(database.Text, nullable=False)
    password = database.Column(database.Text, nullable=False)

    #repr for User class

    def __repr__(self):
        return f"<id={self.id}>"


class Shelter(database.Model):

    __tablename__ = "shelters"


    id= database.Column(database.Integer,primary_key=True,autoincrement=True)
    name = database.Column(database.Text, nullable=False)
    street_address = database.Column(database.Text, nullable=False)
    city = database.Column(database.Text, nullable=False)
    state = database.Column(database.Text, nullable=False)
    zipcode = database.Column(database.Integer, nullable=False)
    website = database.Column(database.Text, nullable=False)

    #relationship between shelter and animal

    animal = database.relationship('Animal',back_populates="shelter")



    #repr for shelter class

    def __repr__(self):
        return f"<id={self.id} name={self.name}>"


if __name__== "__main__":
    #will need to create server file
    from server import app
    database_connect(app, "pawsforalarm")
    # print("database connection established")
