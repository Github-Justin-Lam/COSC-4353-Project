from app import app
import unittest

class FlaskTestCase(unittest.TestCase):

    #LOGIN/REGISTRATION TESTING
    #ensure that flask was set up correctly
    def test_index(self):
        tester = app.test_client(self)
        response = tester.get('/', content_type='html/text')
        self.assertEqual(response.status_code, 200) #request is successful
    
    #ensure that the login page loads correctly
    def test_profile_loads(self):
        tester = app.test_client(self)
        response = tester.get('/', content_type='html/text')
        self.assertTrue(b'Login' in response.data) #check if loaded with the name of page

    #ensure registration behaves correctly given valid field inputs
    def test_correct_form(self):
        tester = app.test_client(self)
        response = tester.post('/register',
            data=dict(email="username@gmail.com",
                    username= "root",
                    password= "123456"
                ))
        self.assertTrue(b'You are now registered and can log in' in response.data)
    
    #ensure login behaves correctly given invalid field inputs
    def test_incorrect_form(self):
        tester = app.test_client(self)
        response = tester.get('/login',
            data=dict(username= "root",
                    password= '126'
                ))
        self.assertTrue(b'Username not found' in response.data)
    
    #PROFILE TESTING
    #ensure that flask was set up correctly
    def test_profile(self):
        with app.test_client() as tester:
            with tester.session_transaction() as sess:
                # Modify the session in this context block.
                sess["username"] = "alex"
            response = tester.get('/profile', content_type='html/text')
            self.assertEqual(response.status_code, 200) #request is successful


    #ensure that the profile page loads correctly
    def test_profile_loads(self):
         with app.test_client() as tester:
            with tester.session_transaction() as sess:
                # Modify the session in this context block.
                sess["username"] = "alex"
            response = tester.get('/profile', content_type='html/text')
            self.assertTrue(b'Client Profile Management' in response.data) #check if loaded with the name of page
   
    #ensure profile behaves correctly given valid field inputs
    def test_correct_form(self):
         with app.test_client() as tester:
            with tester.session_transaction() as sess:
                # Modify the session in this context block.
                sess["username"] = "alex"
            response = tester.post('/profile',
                data=dict(name="alex",
                    address1="5832 broadway street",
                    address2="1976 broadway street",
                    city="houston",
                    state="TX",
                    zip="89935"))
            self.assertTrue(b'Profile Completed!' in response.data)

    def test_address2optional_form(self):
         with app.test_client() as tester:
            with tester.session_transaction() as sess:
                # Modify the session in this context block.
                sess["username"] = "alex"
            response =tester.post('/profile',
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
         with app.test_client() as tester:
            with tester.session_transaction() as sess:
                # Modify the session in this context block.
                sess["username"] = "alex"
            response =tester.post('/profile',
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
         with app.test_client() as tester:
            with tester.session_transaction() as sess:
                # Modify the session in this context block.
                sess["username"] = "alex"
            response =tester.post('/profile',
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
         with app.test_client() as tester:
            with tester.session_transaction() as sess:
                # Modify the session in this context block.
                sess["username"] = "alex"
            response =tester.post('/profile',
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
         with app.test_client() as tester:
            with tester.session_transaction() as sess:
                # Modify the session in this context block.
                sess["username"] = "alex"
            response =tester.post('/profile',
                data=dict(name="alex",
                    address1="5832 broadway street",
                    address2="1976 broadway street",
                    city="",
                    state="TX",
                    zip="89935"),
                follow_redirects=True
            )
            self.assertTrue(b'city is required' in response.data)

    #FUEL QUOTE TESTING

    #Note: Basic profile fields such as name, address 1, address 2, city, state, zip, etc. are already covered by profile management (profileBackend.py / profileTest.py)
    #-and thus do not need to be tested in fuelquoteBackend.py / fuelquoteTest.py

    #ensure that flask was set up correctly
    def test_fuelquote(self):
         with app.test_client() as tester:
            with tester.session_transaction() as sess:
                # Modify the session in this context block.
                sess["username"] = "alex"
            response = tester.get('/fuelquote', content_type='html/text')
            self.assertEqual(response.status_code, 200) #request is successful

    #ensure that page loaded correctly
    def test_fuelquoteform_loads(self):
         with app.test_client() as tester:
            with tester.session_transaction() as sess:
                # Modify the session in this context block.
                sess["username"] = "alex"
            response = tester.get('/fuelquote', content_type='html/text')
            self.assertTrue(b'Fuel Quote Form' in response.data)
    
    #tests gallons empty (invalid)
    def test_gallons_empty_form(self):
        tester = app.test_client(self)
        response = tester.post('/fuelquote', 
            data=dict(gallons = ""))

    #tests gallons negative (invalid)
    def test_gallons_negative_form(self):
        tester = app.test_client(self)
        response = tester.post('/fuelquote', 
            data=dict(gallons = "-5"))

    #tests gallons zero (invalid)
    def test_gallons_zero_form(self):
        tester = app.test_client(self)
        response = tester.post('/fuelquote', 
            data=dict(gallons = "0"))

    #tests gallons positive (valid)
    def test_gallons_positive_form(self):
        tester = app.test_client(self)
        response = tester.post('/fuelquote', 
            data=dict(gallons = "5"))

    #tests delivery_date empty (invalid)
    def test_delivery_date_empty_form(self):
        tester = app.test_client(self)
        response = tester.post('/fuelquote', 
            data=dict(delivery_date = ""))
    
    #tests delivery_date past (invalid)
    def test_delivery_date_past_form(self):
        tester = app.test_client(self)
        response = tester.post('/fuelquote', 
            data=dict(delivery_date = "2022-03-11"))

    #tests delivery_date present (valid)
    def test_delivery_date_present_form(self):
        tester = app.test_client(self)
        response = tester.post('/fuelquote', 
            data=dict(delivery_date = "2022-03-12"))

    #tests delivery_date future (valid)
    def test_delivery_date_future_form(self):
        tester = app.test_client(self)
        response = tester.post('/fuelquote', 
            data=dict(delivery_date = "2023-04-13"))

    #tests gallons (invalid) and delivery_date empty date (invalid)
    def test_both_empty_form(self):
        tester = app.test_client(self)
        response = tester.post('/fuelquote', 
            data=dict(gallons = "", delivery_date = ""))

    #tests gallons negative (invalid) and delivery_date past date (invalid)
    def test_both_invalid_form(self):
        tester = app.test_client(self)
        response = tester.post('/fuelquote', 
            data=dict(gallons = "-6", delivery_date = "2000-03-10"))

    #tests gallons zero (invalid) and delivery_date past date (invalid)
    def test_both_invalid_2_form(self):
        tester = app.test_client(self)
        response = tester.post('/fuelquote', 
            data=dict(gallons = "0", delivery_date = "2000-03-09"))

    #tests gallons positive (valid) and delivery_date future date (valid)
    def test_both_valid_form(self):
        tester = app.test_client(self)
        response = tester.post('/fuelquote', 
            data=dict(gallons = "9", delivery_date = "2055-03-15"))

    #tests gallons positive (valid) and delivery_date past date (invalid)
    def test_valid_invalid_form(self):
        tester = app.test_client(self)
        response = tester.post('/fuelquote', 
            data=dict(gallons = "9", delivery_date = "1999-03-01"))

    #tests gallons zero (invalid) and delivery_date future date (valid)
    def test_invalid_valid_form(self):
        tester = app.test_client(self)
        response = tester.post('/fuelquote', 
            data=dict(gallons = "0", delivery_date = "2222-05-05"))

    #tests gallons negative (invalid) and delivery_date future date (valid)
    def test_invalid_valid_2_form(self):
        tester = app.test_client(self)
        response = tester.post('/fuelquote', 
            data=dict(gallons = "-999", delivery_date = "2223-01-01"))

    #HISTORY TESTING

    #ensure that flask was set up correctly
    def test_history(self):
        with app.test_client() as tester:
            with tester.session_transaction() as sess:
                # Modify the session in this context block.
                sess["username"] = "alex"
            response = tester.get('/history', content_type='html/text')
            self.assertEqual(response.status_code, 200) #request is successful

    #ensure that page loaded correctly
    def test_history_loads(self):
        with app.test_client() as tester:
            with tester.session_transaction() as sess:
                # Modify the session in this context block.
                sess["username"] = "alex"
            response = tester.get('/history', content_type='html/text')
            self.assertTrue(b'Fuel Quote History' in response.data)

if __name__ == '__main__':
    unittest.main()