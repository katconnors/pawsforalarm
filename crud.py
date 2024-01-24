
from model import database, Shelter, Animal, database_connect


#animal functions

def create_animal(api_id, name,image,type,breed,gender, adopt_code,entry_source,shelter,url=None,age=None,join_date=None,weight=None,scheduled_euthanasia_date=None,bio=None):
    """Create shelter animal"""
    
    animal = Animal(api_id=api_id,name=name,image=image,type=type,breed=breed,gender=gender,adopt_code=adopt_code,entry_source=entry_source,shelter=shelter,url=url,age=age,join_date=join_date,weight=weight,scheduled_euthanasia_date=scheduled_euthanasia_date,bio=bio)

    database.session.add(animal)
    database.session.commit()


def view_animals(type,state,sort_type):
    """View animals, with filter ability"""
    
    ani_obj = Animal.query.join(Shelter)

    

    if state =="CA":
        ani_list = ani_obj.filter(Shelter.state=="CA")
    
    elif state =="other":
        ani_list = ani_obj.filter(Shelter.state!="CA")
    
    else:
        ani_list = ani_obj



    if type and type!="all":
        type_filter_animals = ani_list.filter(Animal.type==type)

    else:
        type_filter_animals = ani_list
    
    if sort_type:
        # will also need to add sorting for None items
        final_list = type_filter_animals.order_by(sort_type).all()
    else:
        return type_filter_animals.all()

    return final_list


    

def specific_animal(id):
    """View animal, using id"""
    
    return Animal.query.get(id)


def animal_id_is_in_pfa(api_animalid):
    """Grab the animal api id from PFA database"""

    return bool(Animal.query.filter(Animal.api_id==api_animalid).first())



#shelter functions


def create_shelter(name,street_address,city,state,zipcode,website):
    """Create shelter"""

    #later add if-then statement to check database for already created instance

    shelter = Shelter(name=name,street_address=street_address,city=city,state=state,zipcode=zipcode,website=website)

    database.session.add(shelter)
    database.session.commit()

    return shelter

def edit_shelter_url(name,newurl):
    """Update the url of a shelter"""
    shelter = Shelter.query.filter(Shelter.name==name).first()
    shelter.website = newurl

    database.session.commit()

def specific_shelter(id):
    """View shelter, using id"""
    
    return Shelter.query.get(id)

def give_shelter_names(typed):
    """Return a list of results with shelter names that match a typed string"""
   
    # case insensitive search

    all_type_match = Shelter.query.filter(Shelter.name.ilike(f'%{typed}%')).all()
    list_matching = []

    for shelter in all_type_match:
        list_matching.append({"name":shelter.name,"id": shelter.id})

    return list_matching



def shelter_isthere(compare_name):
    """Check for a shelter in the database, using name
    Result will be true or false"""
   
    return bool(Shelter.query.filter(Shelter.name==compare_name).first())


def shelter_indatabase(compare_name):
    """Check for shelter info, if already present"""
    
    return Shelter.query.filter(Shelter.name==compare_name).first()


if __name__== "__main__":
    
    from server import app
    database_connect(app, "pawsforalarm")