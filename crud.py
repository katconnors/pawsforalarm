
from model import database, Shelter, Animal, database_connect

import itertools


#animal functions

def create_animal(api_id, name,image,type,breed,gender, adopt_code,entry_source,shelter,tracker, avail_date=None, groupstatus=None, status=None, url=None,age=None,join_date=None,weight=None,scheduled_euthanasia_date=None,bio=None):
    """Create shelter animal"""
    
    animal = Animal(
        api_id=api_id,
        name=name,
        image=image,
        type=type,
        breed=breed,
        gender=gender,
        adopt_code=adopt_code,
        entry_source=entry_source,
        shelter=shelter,
        tracker=tracker,
        avail_date=avail_date, 
        groupstatus=groupstatus, 
        status=status,
        url=url,age=age,
        join_date=join_date,
        weight=weight,
        scheduled_euthanasia_date=scheduled_euthanasia_date,
        bio=bio)

    database.session.add(animal)
    database.session.commit()


def view_animals(type="all",query_state="all",group="all",sort_type="scheduled_euthanasia_date"):
    """View animals, with filter ability"""
    
    ani_obj = Animal.query.join(Shelter).filter(Animal.status=="available")


    if query_state and query_state!="all":
        ani_list = ani_obj.filter(Shelter.state==query_state,Animal.status=="available")
    
    else:
        ani_list = ani_obj
        

    if group and group!= "all":
        mod_ani_list = ani_list.filter(Animal.groupstatus==group)

    else:
        mod_ani_list = ani_list


    if type and type!="all":
        type_filter_animals = mod_ani_list.filter(Animal.type==type)

    else:
        type_filter_animals = mod_ani_list
    
    if sort_type:
     
        final_list = type_filter_animals.order_by(sort_type).all()
    else:
        return type_filter_animals.all()

    return final_list

def animal_type_list():
    """Returns a list of animal types that are in the database"""

    #note that this will also include animal types from unavailable status animals

    animaltype_list = database.session.query(Animal.type).distinct().order_by(Animal.type).all()
    
    # used guide on how to flatten lists from https://saturncloud.io/blog/how-to-flatten-a-list-of-lists-in-python/

    ani_typelist = list(itertools.chain(*animaltype_list))

    return ani_typelist
    

def specific_animal(id):
    """View animal, using id"""
    
    return Animal.query.get(id)

def animal_by_apiid(api_id):
    """View animal, using api id"""

    return Animal.query.filter(Animal.api_id==api_id).first()


def animal_id_is_in_pfa(api_animalid):
    """Check if the animal api id is in PFA database"""

    return bool(Animal.query.filter(Animal.api_id==api_animalid).first())


def does_animal_euthdatematch(animal_apiid,compare_date):
    """Check for animal info, if already present"""

    animal = animal_by_apiid(animal_apiid)
    return bool(animal.scheduled_euthanasia_date==compare_date)

def update_animal_euthdate(animal_apiid, newdate):

    """Update animal euthanasia date"""

    animal = animal_by_apiid(animal_apiid)

    animal.scheduled_euthanasia_date = newdate

    database.session.commit()



def update_animal_status(animal, newstatus):

    """Update animal status
    Status will be used a means to display/not display animal information"""

    animal.status = newstatus

    database.session.commit()




#shelter functions


def create_shelter(name,street_address,city,state,zipcode,website,source):
    """Create shelter"""


    shelter = Shelter(name=name,street_address=street_address,city=city,state=state,zipcode=zipcode,website=website,source=source)

    database.session.add(shelter)
    database.session.commit()

    return shelter


def shelter_state_list():
    """Returns a list of states that are in the database"""

    state_list = database.session.query(Shelter.state).distinct().order_by(Shelter.state).all()
    
    # used guide on how to flatten lists from https://saturncloud.io/blog/how-to-flatten-a-list-of-lists-in-python/

    flat_list = list(itertools.chain(*state_list))

    return flat_list


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