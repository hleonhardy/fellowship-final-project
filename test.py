import unittest
import server



class ServerTest(unittest.TestCase):
    """ Route Test for server.py """

    def setUp(self):
        """Runs before the tests"""

         #like localhost:5000, but doesn't load the server
        self.client = server.app.test_client()
        server.app.config['TESTING'] = True
        print "set up complete"


    def test_homepage(self):
        """Tests to make sure the homepage shows"""

        #getting the homepage route
        result = self.client.get('/')
        self.assertIn('About', result.data)
        print "About shows up on homepage"



# **************************************************************************** #

if __name__ == "__main__":
    unittest.main()
