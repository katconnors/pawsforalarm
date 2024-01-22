import requests
import server
import crud
from model import database_connect

database_connect(server.app,"pawsforalarm")


base_url= "https://api.rescuegroups.org/v5"
headers={"Authorization":server.API}
body={
    "data": {
        #filters for animals with available statuses, with kill dates, that have had updates after Nov 2023

        "filters": [
            {
                "fieldName": "statuses.name",
                "operation": "equals",
                "criteria": "Available"
            },
            {
                "fieldName": "animals.updatedDate",
                "operation": "greaterthan",
                "criteria": "2023-11-01T00:00:00Z"
            },
            {
                "fieldName": "animals.killDate",
                "operation": "notblank",
            }
                 
        ]
    }
}

#species functions
def get_api_species_id(animal):
    """Obtain an API species id for one animal entry"""

    spec_id = animal["relationships"]["species"]["data"][0]["id"]
    return spec_id

def get_api_species(spec_id,data):
    """Using an API species id, get the species name"""
    
    for potentialspecies in data["included"]:
        if potentialspecies["id"]==spec_id and potentialspecies["type"]=="species":
            species = potentialspecies["attributes"]["singular"]
    return species

#photo functions
def get_api_photo_id(animal):
    """Obtain an API photo id for one animal entry"""

    photo_id = animal["relationships"]["pictures"]["data"][0]["id"]
    return photo_id

def get_api_photo(photo_id,data):
    """Using an API photo id, obtain photo url"""

    for potentialspecies in data["included"]:
        if potentialspecies["id"]==photo_id and potentialspecies["type"]=="pictures":
            photo = potentialspecies["attributes"]["large"]["url"]
    return photo



def create_animal_from_api(animal, shelter_ob,shelter):
    """Take in data from API and create an animal in the Paws for Alarm database"""

    name= animal["attributes"]["name"]

    photo_id = get_api_photo_id(animal)

    image = get_api_photo(photo_id,data)

    species_num= get_api_species_id(animal)

    species = get_api_species(species_num,data)

    breed= animal["attributes"]["breedString"]

    gender = animal["attributes"]["sex"]

    adopt_code = animal["attributes"]["rescueId"]

    entry_source = "rescue_groups_api"

    generic= shelter_ob["url"]

    #can later include logic to handle site entry that is incomplete

    url = animal["attributes"].get("url", generic)

    shelter = shelter

    age=animal["attributes"].get("ageString")

    # join_date=None
    # skip

    # weight=None
    # skip

    scheduled_euthanasia_date=animal["attributes"].get("killDate")

    bio=animal["attributes"].get("descriptionText")


    crud.create_animal(name=name,image=image,type=species,breed=breed,gender=gender,adopt_code=adopt_code,entry_source=entry_source,shelter=shelter,url=url,age=age,scheduled_euthanasia_date=scheduled_euthanasia_date,bio=bio)


def get_shelter_withapi(data,shelterid_api):

    """Get back a specific shelter object from the API"""
    

    data_inc=data["included"]

    #shelter situation

    for assoc in data_inc:
        if assoc["type"] =="orgs" and assoc["id"] == shelterid_api:
            shelter_ob = assoc["attributes"]

    return shelter_ob

def create_shelter_from_api(shelter_ob):
    """Take in API data and create a shelter in the Paws for Alarm database
    Returned variable is the shelter in the Paws For Alarm database"""

    name= shelter_ob["name"]
    address = shelter_ob["street"]
    city=shelter_ob["city"]
    state=shelter_ob["state"].upper()
    zipcode = shelter_ob["postalcode"]
    website = shelter_ob["url"]

    if not crud.shelter_isthere(name):

        shelter_pfa= crud.create_shelter(name,address,city,state,zipcode,website)

        return shelter_pfa
    
    # if shelter is present
    else:
        shelter_prev = crud.shelter_indatabase(name)

        return shelter_prev

def loop_through_api(data_data):
    
    for animal in data_data:

        #find id of the shelter using the API
        shelterid_api= animal["relationships"]["orgs"]["data"][0]["id"]

        shelter_ob= get_shelter_withapi(data,shelterid_api)

        shelter = create_shelter_from_api(shelter_ob)

        create_animal_from_api(animal,shelter_ob,shelter)

#handle multiple pages of results- note that the API default is to display 25 results per page
page_num=1
while True:
    
    endpt=f"/public/animals/search/available/haspic?page={page_num}&include=pictures,species,orgs&fields[animals]=name,url,sex,rescueId,ageString,breedString,killDate,updatedDate,descriptionText&fields[pictures]=large,small&fields[orgs]=name,street,city,state,postalcode,url"
    url=f"{base_url}{endpt}"
    response= requests.post(url,headers=headers,json=body)
    data=response.json()
    data_data = data["data"]

    loop_through_api(data_data)

    if data["meta"]["pageReturned"] == data["meta"]["pages"]:
        break

    else:
        page_num+= 1



