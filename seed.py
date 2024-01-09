#not sure why classes not working, since model was imported

import os
import model
import server


os.system("dropdb pawsforalarm")
os.system("createdb pawsforalarm")
model.database_connect(server.app,"pawsforalarm")
model.database.create_all()


#test user

# testadmin = User(username='tester', password='test')
# database.session.add(testadmin)
# database.session.commit()



#test animal
#need to follow up on testing the foreign key

# testanimal = Animal(name="Dot",type="dog",breed="gs",age=7,gender="female",adopt_code=1234,entry_source="admin")
# database.session.add(testanimal)
# database.session.commit()




#test shelter

# testshelter = Shelter(name="Test Shelter",street_address="123 Lane", city="Testville",zipcode=12345, website="test.com")
# database.session.add(testshelter)
# database.session.commit()

