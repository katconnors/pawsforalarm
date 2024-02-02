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

    def test_auth(self):
        """Tests for wrong auth code"""

        data = MultiDict({"name":"Test Name", "type":"Test Type", "breed": "Test breed","auth":"123"})
        form = forms.AnimalForm(data)
        self.assertFalse(form.validate())

    def test_Name(self):
        """Tests for missing name resulting in alert"""

        data = MultiDict({"type":"Test Type", "breed": "Test breed","auth":os.environ["password"]})
        form = forms.AnimalForm(data)
        self.assertFalse(form.validate())

    def test_url(self):
        """Tests for incorrect url format resulting in alert"""

        data = MultiDict({"name":"Test Name", "type":"Test Type", "breed": "Test breed","auth":os.environ["password"], "url":"wrongurlformat"})
        form = forms.AnimalForm(data)
        self.assertFalse(form.validate())

    def test_type(self):
        """Tests for missing type resulting in alert"""

        data = MultiDict({"name":"Test Name", "breed": "Test breed","auth":os.environ["password"]})
        form = forms.AnimalForm(data)
        self.assertFalse(form.validate())

    def test_breed(self):
        """Tests for missing breed resulting in alert"""

        data = MultiDict({"name":"Test Name", "type":"Test Type","auth":os.environ["password"]})
        form = forms.AnimalForm(data)
        self.assertFalse(form.validate())


    def test_minForm(self):
        """Checks for minimum completed form leading to a validation"""

        data = MultiDict({"name":"Test Name", "type":"Test Type", "breed": "Test breed","auth":os.environ["password"]})
        form = forms.AnimalForm(data)
        self.assertTrue(form.validate(),form.errors)



if __name__ == "__main__":
    import unittest

    unittest.main()