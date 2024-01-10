
from model import database, Shelter, Animal, database_connect


def create_animal(name,type,breed,age,gender, adopt_code,entry_source,join_date=None,weight=None,scheduled_euthanasia_date=None,bio=None):

    animal = Animal(name=name,type=type,breed=breed,age=age,gender=gender,adopt_code=adopt_code,entry_source=entry_source,join_date=join_date,weight=weight,scheduled_euthanasia_date=scheduled_euthanasia_date,bio=bio)

    database.session.add(animal)
    database.session.commit()

def create_shelter(name,street_address,city,state,zipcode,website):

    shelter = Shelter(name=name,street_address=street_address,city=city,state=state,zipcode=zipcode,website=website)

    database.session.add(shelter)
    database.session.commit()

def view_animals():
    
    return Animal.query.all()


if __name__== "__main__":
    
    from server import app
    database_connect(app, "pawsforalarm")