import server
import unittest
import os

from model import database_connect, database



class IntegrationTests(unittest.TestCase):

    """Tests for the Flask server"""

    #setup to reduce repetition between methods

    def setUp(self):

        self.client = server.app.test_client()

        #consider usiung delete func
        os.system("dropdb testdb")
        os.system("createdb testdb")

    # from testing 1 lecture- printing Flask errors
        server.app.config['TESTING'] = True

    #connecting to a test database
        
        #syntax of database_connect function is such that name of database without postgresql:/// should be the second param 
        database_connect(server.app, "testdb")
        database.create_all()

    #can later add sample data here, if needed for testing
        
        
        

    def test_homepage(self):

        output = self.client.get('/')
        self.assertEqual(output.status_code,200)
        self.assertIn(b'Welcome to Paws for Alarm', output.data)



    def test_faq(self):

        output = self.client.get('/faq')
        self.assertEqual(output.status_code,200)
        self.assertIn(b'FAQ', output.data)


    
        
    def test_animalpage(self):

        output = self.client.get('/animals')
        self.assertEqual(output.status_code,200)
        self.assertIn(b'Animals with Euthanasia Risk Or In Need of Foster', output.data)

        
    def test_animal_wrongauth(self):
        """Checking if the admin page for adding animals returns the appropriate text when an incorrect auth key is given """

        output = self.client.post('/add', data={'auth-code':'1'})
        self.assertEqual(output.status_code,200)
        self.assertIn(b'You need to provide a correct auth key!', output.data)


    def test_shelter_wrongauth(self):
        """Checking if the admin page for adding shelters returns the appropriate text when an incorrect auth key is given """

        output = self.client.post('/addshelter', data={'auth-code':'1'})
        self.assertEqual(output.status_code,200)
        self.assertIn(b'You need to provide a correct auth key!', output.data)



if __name__ == "__main__":
    import unittest

    unittest.main()