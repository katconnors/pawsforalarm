

from flask_sqlalchemy import SQLAlchemy


database= SQLAlchemy()


#using the skeleton for the connection in the sql-alchemy 1 lecture

def database_connect(app,database_name):

    app.config["SQLALCHEMY_DATABASE_URI"] = f"postgresql:///{database_name}"
    app.config["SQLALCHEMY_ECHO"] = True
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    

    database.app = app
    database.init_app(app)


class Animal(database.Model):
    """Animals at risk"""


    __tablename__ = "animals"


    id = database.Column(database.Integer,primary_key=True,autoincrement=True)
    image = database.Column(database.Text, nullable=False)
    name = database.Column(database.Text, nullable=False)
    type = database.Column(database.Text, nullable=False)
    breed = database.Column(database.Text, nullable=False)
    join_date = database.Column(database.Date, nullable=True)
    #age is not an integer in database due to RG API using strings
    age = database.Column(database.Text, nullable=True)
    weight = database.Column(database.Integer, nullable=True)
    gender = database.Column(database.Text, nullable=False)
    scheduled_euthanasia_date = database.Column(database.Date, nullable=True)
    adopt_code = database.Column(database.Text, nullable=False)
    bio = database.Column(database.Text, nullable=True)
    url = database.Column(database.Text, nullable=False)
    entry_source = database.Column(database.Text, nullable=False)
    shelter_id = database.Column(database.Integer, database.ForeignKey('shelters.id'))

    #relationship between animal and shelter

    shelter = database.relationship('Shelter',back_populates="animal")


    def __repr__(self):
        return f"<id={self.id} name={self.name} type={self.type}>"
    
class User(database.Model):
    """Admin user"""

    __tablename__ = "users"
    
    id = database.Column(database.Integer,primary_key=True,autoincrement=True)
    username = database.Column(database.Text, nullable=False)
    password = database.Column(database.Text, nullable=False)


    def __repr__(self):
        return f"<id={self.id}>"


class Shelter(database.Model):
    """Shelters that have animals at risk"""

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


    def __repr__(self):
        return f"<id={self.id} name={self.name}>"


if __name__== "__main__":

    from server import app
    database_connect(app, "pawsforalarm")
    # print("database connection established")
