
from model import database, Shelter, Animal, database_connect

#nice to have func's
#deletion func
#edit field function




#follow up on shelter id
def create_animal(name,image,type,breed,gender, adopt_code,entry_source,shelter,url,age=None,join_date=None,weight=None,scheduled_euthanasia_date=None,bio=None):
    # make sure to use a full http link for animal url
    animal = Animal(name=name,image=image,type=type,breed=breed,gender=gender,adopt_code=adopt_code,entry_source=entry_source,shelter=shelter,url=url,age=age,join_date=join_date,weight=weight,scheduled_euthanasia_date=scheduled_euthanasia_date,bio=bio)

    database.session.add(animal)
    database.session.commit()

def create_shelter(name,street_address,city,state,zipcode,website):

    #if-then statement to check database for already created instance

    shelter = Shelter(name=name,street_address=street_address,city=city,state=state,zipcode=zipcode,website=website)

    database.session.add(shelter)
    database.session.commit()

    return shelter

def view_animals(type,state):

    
    # update code when common states are assessed

    if type and (state =="ca"):
        return Animal.query.join(Shelter).filter(Shelter.state=="ca",Animal.type==type).all()
    
    elif type and (state !="ca"):
        return Animal.query.join(Shelter).filter(Shelter.state!="ca", Animal.type==type).all()
    

    else:
        return Animal.query.all()

def specific_shelter(id):
    
    return Shelter.query.get(id)

def specific_animal(id):
    
    return Animal.query.get(id)

if __name__== "__main__":
    
    from server import app
    database_connect(app, "pawsforalarm")