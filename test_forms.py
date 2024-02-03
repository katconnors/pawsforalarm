import unittest
import os
import forms
import server
from werkzeug.datastructures import MultiDict

class FormTest(unittest.TestCase):

    
    def setUp(self):

        # stack overflow resource for app_context https://stackoverflow.com/questions/55427943/unit-test-fails-on-wtforms

        self.app_context = server.app.app_context()
        self.app_context.push()
        server.app.config['TESTING'] = True
        server.app.config['WTF_CSRF_ENABLED']  = False

    def tearDown(self):
        self.app_context.pop()


    #tests for add animal 
        
    def test_auth_animal(self):
        """Tests for wrong auth code in add animal route"""

        data = MultiDict({"name":"Test Name", "type":"Test Type", "breed": "Test breed","auth":"123"})
        form = forms.AnimalForm(data)
        self.assertFalse(form.validate())

    def test_Name_animal(self):
        """Tests for missing name resulting in alert in add animal route"""

        data = MultiDict({"type":"Test Type", "breed": "Test breed","auth":os.environ["password"]})
        form = forms.AnimalForm(data)
        self.assertFalse(form.validate())

    def test_url_animal(self):
        """Tests for incorrect url format resulting in alert in add animal route"""

        data = MultiDict({"name":"Test Name", "type":"Test Type", "breed": "Test breed","auth":os.environ["password"], "url":"wrongurlformat"})
        form = forms.AnimalForm(data)
        self.assertFalse(form.validate())

    def test_type_animal(self):
        """Tests for missing type resulting in alert in add animal route"""

        data = MultiDict({"name":"Test Name", "breed": "Test breed","auth":os.environ["password"]})
        form = forms.AnimalForm(data)
        self.assertFalse(form.validate())

    def test_breed_animal(self):
        """Tests for missing breed resulting in alert in add animal route"""

        data = MultiDict({"name":"Test Name", "type":"Test Type","auth":os.environ["password"]})
        form = forms.AnimalForm(data)
        self.assertFalse(form.validate())


    def test_minForm_animal(self):
        """Checks for minimum completed form leading to a validation in add animal route"""

        data = MultiDict({"name":"Test Name", "type":"Test Type", "breed": "Test breed","auth":os.environ["password"]})
        form = forms.AnimalForm(data)
        self.assertTrue(form.validate(),form.errors)



    #tests for add shelter
        
    def test_minForm_shelter(self):
        """Checks for minimum completed form leading to a validation in add shelter route"""

        data = MultiDict({"name":"Test Shelter", "city":"Test city", "state": "state","zipcode": "12345","auth":os.environ["password"]})
        form = forms.ShelterForm(data)
        self.assertTrue(form.validate(),form.errors)

    def test_auth_shelter(self):
        """Tests for wrong auth code in add shelter route"""

        data = MultiDict({"name":"Test Shelter", "city":"Test city", "state": "state","zipcode": "12345","auth":"123"})
        form = forms.ShelterForm(data)
        self.assertFalse(form.validate())

    def test_name_shelter(self):
        """Tests for missing name resulting in alert in add shelter route"""

        data = MultiDict({"city":"Test city", "state": "state","zipcode": "12345","auth":os.environ["password"]})
        form = forms.ShelterForm(data)
        self.assertFalse(form.validate())

    def test_city_shelter(self):
        """Tests for missing city resulting in alert in add shelter route"""

        data = MultiDict({"name":"Test Shelter", "state": "state","zipcode": "12345","auth":os.environ["password"]})
        form = forms.ShelterForm(data)
        self.assertFalse(form.validate())

    def test_state_shelter(self):
        """Tests for missing state resulting in alert in add shelter route"""

        data = MultiDict({"name":"Test Shelter","city":"Test city", "zipcode": "12345","auth":os.environ["password"]})
        form = forms.ShelterForm(data)
        self.assertFalse(form.validate())

    def test_zipcode_shelter(self):
        """Tests for missing zipcode resulting in alert in add shelter route"""

        data = MultiDict({"name":"Test Shelter","city":"Test city", "state": "state","auth":os.environ["password"]})
        form = forms.ShelterForm(data)
        self.assertFalse(form.validate())
        


if __name__ == "__main__":
    import unittest

    unittest.main()