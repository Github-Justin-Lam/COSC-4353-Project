from profileBackend import app
import unittest

"""
coverage run -m profileTest
coverage report -m

Name                Stmts   Miss  Cover   Missing
-------------------------------------------------
profileBackend.py      39      4    90%   23-24, 31-32
profileTest.py         37      0   100%
-------------------------------------------------
TOTAL                  76      4    95%
"""

class FlaskTestCase(unittest.TestCase):

    #ensure that flask was set up correctly
    def test_index(self):
        tester = app.test_client(self)
        response = tester.get('/', content_type='html/text')
        self.assertEqual(response.status_code, 200) #request is successful
    
    #ensure that the profile page loads correctly
    def test_profile_loads(self):
        tester = app.test_client(self)
        response = tester.get('/', content_type='html/text')
        self.assertTrue(b'Client Profile Management' in response.data) #check if loaded with the name of page
    
    #ensure profile behaves correctly given valid field inputs
    def test_correct_form(self):
        tester = app.test_client(self)
        response = tester.post('/',
            data=dict(name="alex",
                address1="5832 broadway street",
                address2="1976 broadway street",
                city="houston",
                state="TX",
                zip="89935"))
        self.assertTrue(b'Profile Completed!' in response.data)

    def test_address2optional_form(self):
        tester = app.test_client(self)
        response =tester.post('/',
            data=dict(name="alex",
                address1="5832 broadway street",
                address2="",
                city="houston",
                state="TX",
                zip="89935"),
            follow_redirects=True
        )
        self.assertTrue(b'Profile Completed!' in response.data)
    
    def test_zipcodeLength_form(self):
        tester = app.test_client(self)
        response =tester.post('/',
            data=dict(name="alex",
                address1="5832 broadway street",
                address2="",
                city="houston",
                state="TX",
                zip="89"),
            follow_redirects=True
        )
        self.assertTrue(b'zipcode is required' in response.data)
    
    def test_nameRequirement_form(self):
        tester = app.test_client(self)
        response =tester.post('/',
            data=dict(name="",
                address1="5832 broadway street",
                address2="1976 broadway street",
                city="houston",
                state="TX",
                zip="89935"),
            follow_redirects=True
        )
        self.assertTrue(b'name is required' in response.data)
    
    def test_addressRequirement_form(self):
        tester = app.test_client(self)
        response =tester.post('/',
            data=dict(name="alex",
                address1="",
                address2="1976 broadway street",
                city="houston",
                state="TX",
                zip="89935"),
            follow_redirects=True
        )
        self.assertTrue(b'address is required' in response.data)
    
    def test_cityRequirement_form(self):
        tester = app.test_client(self)
        response =tester.post('/',
            data=dict(name="alex",
                address1="5832 broadway street",
                address2="1976 broadway street",
                city="",
                state="TX",
                zip="89935"),
            follow_redirects=True
        )
        self.assertTrue(b'city is required' in response.data)

if __name__ == '__main__':
    unittest.main()