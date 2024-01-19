
from model import database, Shelter, Animal, database_connect


#follow up on shelter id
def create_animal(name,image,type,breed,gender, adopt_code,entry_source,shelter,url,age=None,join_date=None,weight=None,scheduled_euthanasia_date=None,bio=None):
    """Create shelter animal"""
    
    animal = Animal(name=name,image=image,type=type,breed=breed,gender=gender,adopt_code=adopt_code,entry_source=entry_source,shelter=shelter,url=url,age=age,join_date=join_date,weight=weight,scheduled_euthanasia_date=scheduled_euthanasia_date,bio=bio)

    database.session.add(animal)
    database.session.commit()

def create_shelter(name,street_address,city,state,zipcode,website):
    """Create shelter"""

    #later add if-then statement to check database for already created instance

    shelter = Shelter(name=name,street_address=street_address,city=city,state=state,zipcode=zipcode,website=website)

    database.session.add(shelter)
    database.session.commit()

    return shelter

def view_animals(type,state):
    """View animals, with filter ability"""
    
    # update code when common states are assessed

    if type and (state =="CA"):
        return Animal.query.join(Shelter).filter(Shelter.state=="CA",Animal.type==type).all()
    
    elif type and (state !="CA"):
        return Animal.query.join(Shelter).filter(Shelter.state!="CA", Animal.type==type).all()
    

    else:
        return Animal.query.all()

def specific_shelter(id):
    """View shelter, using id"""
    
    return Shelter.query.get(id)

def specific_animal(id):
    """View animal, using id"""
    
    return Animal.query.get(id)

if __name__== "__main__":
    
    from server import app
    database_connect(app, "pawsforalarm")