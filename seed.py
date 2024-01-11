
import os
from model import User,Shelter,Animal,database,database_connect
import server

#warning, will drop the db
os.system("dropdb pawsforalarm")
os.system("createdb pawsforalarm")


database_connect(server.app,"pawsforalarm")
database.create_all()


#test user

pfaadmin = User(username='pfaadmin', password=os.environ["password"])
database.session.add(pfaadmin)
database.session.commit()


#test shelter

testshelter = Shelter(name="Test Shelter",street_address="123 Lane", city="Testville",state="CA",zipcode=12345, website="test.com")
database.session.add(testshelter)
database.session.commit()


#test animal

testanimal = Animal(name="Dot",type="dog",breed="gs",age=7,gender="female",adopt_code=1234,url="dog.com",entry_source="admin",shelter_id=testshelter.id)
database.session.add(testanimal)
database.session.commit()



#various test data 

# create_shelter(name="Second Chance", street_address="123 Lane", city="Testville", state="CA", zipcode=334567,website="secondchance.com")
# create_shelter(name="Paws Shelter", street_address="123 Street", city="Test", state="WA", zipcode=334566,website="secondchance.com")


# create_animal(name="Pippi",type="dog",breed="retriever",age=11, gender="female",adopt_code=12524,entry_source="admin",url="animalurl.com",shelter=shelter, bio="test bio",weight=82,scheduled_euthanasia_date="04/12/2025",join_date="01/10/2024")
#  create_animal(name="Potato",type="cat",breed="American Shorthair",age=15, gender="female",adopt_code=14524,entry_source="admin",url="animal2url.com",shelter=shelter, bio="test bio",weight=10,scheduled_euthanasia_date="04/02/2025",join_date="01/10/2024")
# create_animal(name="Donald",type="dog",breed="pitbull",age=5, gender="male",adopt_code=1454,entry_source="admin",url="animal32url.com",shelter=shelter, bio="test bio",weight=60,scheduled_euthanasia_date="04/02/2025",join_date="01/10/2024")
# create_animal(name="Ronald",type="dog",breed="lab",age=5, gender="male",adopt_code=19454,entry_source="admin",url="animal3url.com",shelter=shelter, bio="test bio",weight=90,scheduled_euthanasia_date="04/02/2025",join_date="01/10/2024")
# create_animal(name="Linguine",type="cat",breed="mix",age=12, gender="female",adopt_code="A123",entry_source="admin",url="animal34url.com",shelter=shelter, bio="test bio",weight=8,scheduled_euthanasia_date="05/02/2025",join_date="01/10/2024")
# create_animal(name="Noir",type="cat",breed="mix",age=10, gender="male",adopt_code="A143",entry_source="admin",url="animal34url.com",shelter=shelter, bio="test bio",weight=8,scheduled_euthanasia_date="06/02/2025",join_date="01/10/2024")
# create_animal(name="Nori",type="dog",breed="boxer",age=12, gender="male",adopt_code=19454,entry_source="admin",url="animal3url.com",shelter=shelter, bio="test bio",weight=45,scheduled_euthanasia_date="04/02/2025",join_date="01/10/2024")
# create_animal(name="Popcorn",type="cat",breed="mix",age=15, gender="male",adopt_code=19454,entry_source="admin",url="animal3url.com",shelter=shelter, bio="test bio",weight=8,scheduled_euthanasia_date="04/02/2025",join_date="01/10/2024")