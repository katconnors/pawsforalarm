import server
import unittest



class IntegrationTests(unittest.TestCase):

    """Tests for the Flask server"""

    #setup to reduce repetition between methods

    def setUp(self):

        self.client = server.app.test_client()

    # from testing 1 lecture- printing Flask errors
        server.app.config['TESTING'] = True


    def test_homepage(self):

        output = self.client.get('/')
        self.assertIn(b'Welcome to Paws for Alarm', output.data)


if __name__ == "__main__":
    import unittest

    unittest.main()