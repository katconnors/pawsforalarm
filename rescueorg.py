import requests
import server
import crud
from model import database_connect

database_connect(server.app, "pawsforalarm")


base_url = "https://api.rescuegroups.org/v5"
headers = {"Authorization": server.API}
body = {
    "data": {
        # filters for animals with available statuses, with euthanasia dates or needing foster, that have had updates after Nov 2023
        "filters": [
            {
                "fieldName": "statuses.name",
                "operation": "equals",
                "criteria": "Available",
            },
            {
                "fieldName": "animals.updatedDate",
                "operation": "greaterthan",
                "criteria": "2023-11-01T00:00:00Z",
            },
            {
                "fieldName": "animals.killDate",
                "operation": "notblank",
            },
            {
                "fieldName": "animals.isNeedingFoster",
                "operation": "equals",
                "criteria": "True",
            },
        ],
        "filterProcessing": "1 AND 2 AND (3 OR 4)",
    }
}


class RescueGroupsAnimalFetcher:

    def __init__(self):
        self.indiv_num_tracker = set()

    @staticmethod
    def get_api_species_id(animal):
        """Obtain an API species id for one animal entry"""

        spec_id = animal["relationships"]["species"]["data"][0]["id"]
        return spec_id

    @staticmethod
    def get_api_species(spec_id, data):
        """Using an API species id, get the species name"""

        for potentialspecies in data["included"]:
            if (
                potentialspecies["id"] == spec_id
                and potentialspecies["type"] == "species"
            ):
                species = potentialspecies["attributes"]["singular"]
        return species

    @staticmethod
    def get_api_photo_id(animal):
        """Obtain an API photo id for one animal entry"""
        try:

            photo_id = animal["relationships"]["pictures"]["data"][0]["id"]
            return photo_id

        except KeyError:
            print("There is no photo id.")
            photo_id = None
            return photo_id

    @staticmethod
    def get_api_photo(photo_id, data):
        """Using an API photo id, obtain photo url"""
        if photo_id is not None:
            for potentialspecies in data["included"]:
                if (
                    potentialspecies["id"] == photo_id
                    and potentialspecies["type"] == "pictures"
                ):
                    photo = potentialspecies["attributes"]["large"]["url"]
            return photo
        else:
            photo = None
            return photo

    def create_animal_from_api(self, animal, shelter):
        """Take in data from API and create an animal in the Paws for Alarm database
        Additionally, add to list of newly created animals"""

        name = animal["attributes"]["name"]

        api_id = animal["id"]

        photo_id = self.get_api_photo_id(animal)

        image = self.get_api_photo(photo_id, data)

        species_num = self.get_api_species_id(animal)

        species = self.get_api_species(species_num, data)

        breed = animal["attributes"]["breedString"]

        gender = animal["attributes"].get("sex")

        adopt_code = animal["attributes"].get("rescueId")

        entry_source = "rescue_groups_api"

        url = animal["attributes"].get("url")

        shelter = shelter

        # provides data to shelters regarding where their animals are being viewed
        tracker = animal["attributes"]["trackerimageUrl"]

        avail_date = animal["attributes"].get("availableDate")

        age = animal["attributes"].get("ageString")

        status = "available"

        scheduled_euthanasia_date = animal["attributes"].get("killDate")

        if scheduled_euthanasia_date:
            groupstatus = "euthanasiadates"

        elif animal["attributes"]["isNeedingFoster"] == True:
            groupstatus = "fosterrequests"

        else:
            groupstatus = "other"

        bio = animal["attributes"].get("descriptionText")

        # conditional for prevention of duplicates here

        if crud.animal_id_is_in_pfa(api_id):
            if not crud.does_animal_euthdatematch(api_id, scheduled_euthanasia_date):
                crud.update_animal_euthdate(api_id, scheduled_euthanasia_date)

        else:
            crud.create_animal(
                api_id=api_id,
                name=name,
                image=image,
                type=species,
                breed=breed,
                gender=gender,
                adopt_code=adopt_code,
                entry_source=entry_source,
                shelter=shelter,
                tracker=tracker,
                avail_date=avail_date,
                groupstatus=groupstatus,
                status=status,
                url=url,
                age=age,
                scheduled_euthanasia_date=scheduled_euthanasia_date,
                bio=bio,
            )

        self.indiv_num_tracker.add(api_id)

    @staticmethod
    def check_pfa_vs_apianimals():

        # create a list of all the animal api id's

        pfa_available_animals = set()

        all_statuses_pfa_animals = crud.view_animals()

        for pfa_animal in all_statuses_pfa_animals:
            if pfa_animal.status == "available" and pfa_animal.entry_source != "admin":
                pfa_available_animals.add(pfa_animal.api_id)

        return pfa_available_animals

    def get_all_animal_ids(self):
        return self.indiv_num_tracker


class RescueGroupsShelterFetcher:
    @staticmethod
    def get_shelter_withapi(data, shelterid_api):
        """Get back a specific shelter object from the API"""

        data_inc = data["included"]

        for assoc in data_inc:
            if assoc["type"] == "orgs" and assoc["id"] == shelterid_api:
                shelter_ob = assoc["attributes"]

        return shelter_ob

    @staticmethod
    def create_shelter_from_api(shelter_ob):
        """Take in API data and create a shelter in the Paws for Alarm database
        Returned variable is the shelter in the Paws For Alarm database"""

        name = shelter_ob["name"]
        address = shelter_ob.get("street")
        city = shelter_ob["city"]
        state = shelter_ob["state"].upper()
        zipcode = shelter_ob["postalcode"]
        website = shelter_ob.get("url")
        source = "rescue_groups_api"

        # this bit of code is to handle situations where a rescue has entered this specific string

        if website == "http://":
            website = None

        if not crud.shelter_isthere(name):

            shelter_pfa = crud.create_shelter(
                name, address, city, state, zipcode, website, source
            )

            return shelter_pfa

        else:
            shelter_prev = crud.shelter_indatabase(name)

            return shelter_prev


def loop_through_api(data_data):

    new_animal_fetcher = RescueGroupsAnimalFetcher()
    new_shelter_fetcher = RescueGroupsShelterFetcher()

    for animal in data_data:

        # find id of the shelter using the API

        shelterid_api = animal["relationships"]["orgs"]["data"][0]["id"]

        shelter_ob = new_shelter_fetcher.get_shelter_withapi(data, shelterid_api)

        shelter = new_shelter_fetcher.create_shelter_from_api(shelter_ob)

        new_animal_fetcher.create_animal_from_api(animal, shelter)

    return new_animal_fetcher.get_all_animal_ids()


def mark_unavailable(animal_ids):
    pfa_available_animals = RescueGroupsAnimalFetcher.check_pfa_vs_apianimals()

    # this result will give the animals that no longer appear in api results, but are still in the pfa database
    set_differences = pfa_available_animals - animal_ids

    for api_id in set_differences:

        animal = crud.animal_by_apiid(api_id)
        crud.update_animal_status(animal, "not available")


unavailable_animal_ids = set()

page_num = 1
while True:

    endpt = f"/public/animals/search/available/haspic?page={page_num}&include=pictures,species,orgs&fields[animals]=name,url,trackerimageUrl, availableDate,sex,rescueId,ageString,breedString,killDate,isNeedingFoster,updatedDate,descriptionText&fields[pictures]=large,small&fields[orgs]=name,street,city,state,postalcode,url"
    url = f"{base_url}{endpt}"
    response = requests.post(url, headers=headers, json=body)
    data = response.json()
    data_data = data["data"]

    individual_num_tracker = loop_through_api(data_data)

    unavailable_animal_ids.update(individual_num_tracker)

    if data["meta"]["pageReturned"] == data["meta"]["pages"]:
        break

    else:
        page_num += 1

mark_unavailable(unavailable_animal_ids)
