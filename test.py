import unittest
import server
from model import connect_to_db, db
from seed_testdb import load_test_data



class ServerTest(unittest.TestCase):
    """ Route Test for server.py """

    def setUp(self):
        """Runs before the tests"""

        #connect to app using test database
        connect_to_db(server.app, "postgresql:///testdb")

        db.create_all()
        load_test_data()

         #like localhost:5000, but doesn't load the server
        self.client = server.app.test_client()
        server.app.config['TESTING'] = True
        server.app.config['SECRET_KEY'] = 'key'

        # with self.client as c:
        #     with c.session_transaction() as sess:
        #         sess['current_user'] = 1

        print "set up complete"


    def tearDown(self):
        """ Gets rid of everything """

        db.session.close()
        db.drop_all()

        print "tear down complete"


    def test_homepage(self):
        """ Tests to make sure the homepage shows"""

        #getting the homepage route
        result = self.client.get('/')
        self.assertIn('<h2> About: </h2>', result.data)
        print "Homepage Route Successful"


    def test_location(self):
        """ Tests the 'Advanced Search' page. """

        #getting the location route
        result = self.client.get('/location')
        self.assertIn('<h1> Advanced Search </h1>', result.data)
        print "Advanced Search Route Successful"


    def test_prediction(self):
        """ Tests the actual prediction page. """

        sfprediction = '/prediction?lat=37.6189994812012&lon=-122.375'
        result = self.client.get(sfprediction)

        self.assertIn('<h1> Here is my prediction: </h1>', result.data)

        print "Gave SF lat and lng, got prediction route to show."


    def test_register_page(self):
        """ Tests registration page. """

        result = self.client.get('/register')
        self.assertIn('<td>Name: </td>', result.data)

        print "Registration Route Successful."


    def test_login_page(self):
        """ Tests log in page """

        result = self.client.get('/login')
        self.assertIn('<h1>Log In!</h1>', result.data)

        print "Log In Route Successful"



    def test_login_process(self):
        """ Tests to see if a user can successfully log in. """

        result = self.client.post('/login',
                                    data={'email': 'sbob78@gmail.com', 'password': 'password'},
                                    follow_redirects=True)
        self.assertIn('Log Out', result.data)

        print "User Successfully Logged In"


    def test_my_page(self):
        """ Tests the user's page """

        with self.client as c:
            with c.session_transaction() as sess:
                sess['current_user'] = 1

        result = self.client.get('/mypage')
        self.assertIn('<h3> Favorite Locations: </h3>', result.data)

        print 'My Page Route Successful'


    def test_my_page_not_logged_in(self):
        """ Does it redirect to home if user is not logged in"""

        result = self.client.get('/mypage', follow_redirects=True)
        self.assertIn('<h2> About: </h2>', result.data)

        print "My Page Not Accessable to Not Logged In User"


    def test_add_fav_route(self):
        """Tests to see if the favorites page shows up"""

        result = self.client.get('/addfavorite')
        self.assertIn('')



# **************************************************************************** #

if __name__ == "__main__":
    unittest.main()
