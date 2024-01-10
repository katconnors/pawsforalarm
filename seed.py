
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
#need to follow up on testing the foreign key

testanimal = Animal(name="Dot",type="dog",breed="gs",age=7,gender="female",adopt_code=1234,entry_source="admin",shelter_id=testshelter.id)
database.session.add(testanimal)
database.session.commit()

