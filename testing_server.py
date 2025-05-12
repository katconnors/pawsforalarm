import server
import unittest
import os

from model import database_connect, database


class IntegrationTests(unittest.TestCase):
    """Tests for the Flask server"""

    # setup to reduce repetition between methods
    @classmethod
    def setUpClass(cls):

        os.system("dropdb testdb")
        os.system("createdb testdb")

        # from testing 1 lecture- printing Flask errors
        server.app.config["TESTING"] = True

        # connecting to a test database

        # syntax of database_connect function is such that name of database without postgresql:/// should be the second param
        database_connect(server.app, "testdb")
        database.create_all()

        cls.client = server.app.test_client()

    def test_homepage(self):
        """Testing for homepage success"""

        output = self.client.get("/")
        self.assertEqual(output.status_code, 200)
        self.assertIn(b"Welcome to Paws For Alarm", output.data)

    def test_faq(self):
        """Testing for FAQ page success"""

        output = self.client.get("/faq")
        self.assertEqual(output.status_code, 200)
        self.assertIn(b"FAQ", output.data)

    def test_animalpage(self):
        """Testing for animal list page success"""

        output = self.client.get("/animals")
        self.assertEqual(output.status_code, 200)
        self.assertIn(b"Animals with Euthanasia Risk Or In Need of Foster", output.data)


if __name__ == "__main__":
    import unittest

    unittest.main()
