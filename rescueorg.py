import requests
import os
import server
import crud
from model import database_connect, database

database_connect(server.app,"pawsforalarm")


base_url= "https://api.rescuegroups.org/v5"
endpt="/public/animals/search/available/haspic?limit=1&include=pictures,species,orgs&fields[animals]=name,url,sex,rescueId,ageString,breedString,killDate,updatedDate,descriptionText&fields[pictures]=large,small&fields[orgs]=name,street,city,state,postalcode,url"
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



#name 
#note that this is just the first entry and will need a loop
# data["data"][0]["attributes"]["name"]



def api_shelter(data):

    name = data["included"][-1]["attributes"]["name"]

    address = data["included"][-1]["attributes"]["street"]

    city= data["included"][-1]["attributes"]["city"]

    state= data["included"][-1]["attributes"]["state"]

    zipcode = data["included"][-1]["attributes"]["postalcode"]

    website = data["included"][-1]["attributes"]["url"]

    
    shelter= crud.create_shelter(name,address,city,state,zipcode,website)

    return shelter

def api_animal(shelterid,data):

    name= data["data"][0]["attributes"]["name"]


    image = data["included"][0]["attributes"]["large"]["url"]

    type = data["included"][-2]["attributes"]["singular"]

    breed= data["data"][0]["attributes"]["breedString"]

    gender = data["data"][0]["attributes"]["sex"]

    adopt_code = data["data"][0]["attributes"]["rescueId"]

    entry_source = "rescue_groups_api"
    generic= data["included"][-1]["attributes"]["url"]
    url = data["data"][0]["attributes"].get("url", generic)

    shelter = crud.specific_shelter(shelterid)

    age=data["data"][0]["attributes"].get("ageString")

    # join_date=None
    # skip

    # weight=None
    # skip

    scheduled_euthanasia_date=data["data"][0]["attributes"].get("killDate")

    bio=data["data"][0]["attributes"].get("descriptionText")


    crud.create_animal(name=name,image=image,type=type,breed=breed,gender=gender,adopt_code=adopt_code,entry_source=entry_source,shelter=shelter,url=url,age=age,scheduled_euthanasia_date=scheduled_euthanasia_date,bio=bio)

shelter_obj = api_shelter(data)

#will need to have some some of if statement to prevent duplicates
id= shelter_obj.id

api_animal(id, data)
