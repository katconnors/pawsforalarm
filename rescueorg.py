import requests
import os
import server
import crud
from model import database_connect, database
import pprint

database_connect(server.app,"pawsforalarm")


base_url= "https://api.rescuegroups.org/v5"
endpt="/public/animals/search/available/haspic?include=pictures,species,orgs&fields[animals]=name,url,sex,rescueId,ageString,breedString,killDate,updatedDate,descriptionText&fields[pictures]=large,small&fields[orgs]=name,street,city,state,postalcode,url"
headers={"Authorization":server.API}
url=f"{base_url}{endpt}"
body={
    "data": {
        "filters": [
            {
                "fieldName": "statuses.name",
                "operation": "equals",
                "criteria": "Available"
            },
            {
                "fieldName": "animals.updatedDate",
                "operation": "greaterthan",
                "criteria": "2024-01-01T00:00:00Z"
            },
            {
                "fieldName": "animals.killDate",
                "operation": "notblank",
            }
            # ,
            # {   "fieldName": "animals.url",
            #     "operation": "notblank",
            # }        
        ]
    }
}
response= requests.post(url,headers=headers,json=body)
data=response.json()





data_data = data["data"]

def get_species_id(animal):
    spec_id = animal["relationships"]["species"]["data"][0]["id"]
    return spec_id

def get_species(spec_id):
    
    for potentialspecies in data["included"]:
        if potentialspecies["id"]==spec_id and potentialspecies["type"]=="species":
            species = potentialspecies["attributes"]["singular"]
    return species

def get_photo_id(animal):
    photo_id = animal["relationships"]["pictures"]["data"][0]["id"]
    return photo_id

def get_photo(photo_id):
    
    for potentialspecies in data["included"]:
        if potentialspecies["id"]==photo_id and potentialspecies["type"]=="pictures":
            photo = potentialspecies["attributes"]["large"]["url"]
    return photo



def api_animal(animal, shelter_ob,shelter):


    name= animal["attributes"]["name"]

    photo_id = get_photo_id(animal)

    image = get_photo(photo_id)

    species_num= get_species_id(animal)

    species = get_species(species_num)

    breed= animal["attributes"]["breedString"]

    gender = animal["attributes"]["sex"]

    adopt_code = animal["attributes"]["rescueId"]

    entry_source = "rescue_groups_api"

    generic= shelter_ob["url"]
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

    #getting back a specific shelter object from the API
    

    data_inc=data["included"]

    #shelter situation

    for assoc in data_inc:
        if assoc["type"] =="orgs" and assoc["id"] == shelterid_api:
            shelter_ob = assoc["attributes"]

    return shelter_ob

def api_shelter(shelter_ob):

    name= shelter_ob["name"]
    address = shelter_ob["street"]
    city=shelter_ob["city"]
    state=shelter_ob["state"]
    zipcode = shelter_ob["postalcode"]
    website = shelter_ob["url"]

    
    shelter_pfa= crud.create_shelter(name,address,city,state,zipcode,website)

    return shelter_pfa

def loop_through_api():
    #find id of the shelter using the API

    for animal in data_data:

        shelterid_api= animal["relationships"]["orgs"]["data"][0]["id"]

        shelter_ob= get_shelter_withapi(data,shelterid_api)

        shelter = api_shelter(shelter_ob)

        api_animal(animal,shelter_ob,shelter)





#will need to have some some of if statement to prevent duplicates


# will need to prevent duplicates here as well
# additionally, will need a delete functionality if entries no longer appear in api request results


loop_through_api()
