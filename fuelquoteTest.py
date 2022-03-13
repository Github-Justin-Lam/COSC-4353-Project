from fuelquoteBackend import app
import unittest

"""
Name                  Stmts   Miss  Cover   Missing
---------------------------------------------------
fuelquoteBackend.py      32      0   100%
fuelquoteTest.py         59      0   100%
---------------------------------------------------
TOTAL                    91      0   100%
"""

class FlaskTestCase(unittest.TestCase):

    #Note: Basic profile fields such as name, address 1, address 2, city, state, zip, etc. are already covered by profile management (profileBackend.py / profileTest.py)
    #-and thus do not need to be tested in fuelquoteBackend.py / fuelquoteTest.py

    #ensure that flask was set up correctly
    def test_index(self):
        tester = app.test_client(self)
        response = tester.get('/', content_type='html/text')
        self.assertEqual(response.status_code, 200) #request is successful

    #ensure that page loaded correctly
    def test_fuelquoteform_loads(self):
        tester = app.test_client(self)
        response = tester.get('/', content_type='html/text')
        self.assertTrue(b'Fuel Quote Form' in response.data)
    
    #tests gallons empty (invalid)
    def test_gallons_empty_form(self):
        tester = app.test_client(self)
        response = tester.post('/', 
            data=dict(gallons = ""))

    #tests gallons negative (invalid)
    def test_gallons_negative_form(self):
        tester = app.test_client(self)
        response = tester.post('/', 
            data=dict(gallons = "-5"))

    #tests gallons zero (invalid)
    def test_gallons_zero_form(self):
        tester = app.test_client(self)
        response = tester.post('/', 
            data=dict(gallons = "0"))

    #tests gallons positive (valid)
    def test_gallons_positive_form(self):
        tester = app.test_client(self)
        response = tester.post('/', 
            data=dict(gallons = "5"))

    #tests delivery_date empty (invalid)
    def test_delivery_date_empty_form(self):
        tester = app.test_client(self)
        response = tester.post('/', 
            data=dict(delivery_date = ""))
    
    #tests delivery_date past (invalid)
    def test_delivery_date_past_form(self):
        tester = app.test_client(self)
        response = tester.post('/', 
            data=dict(delivery_date = "2022-03-11"))

    #tests delivery_date present (valid)
    def test_delivery_date_present_form(self):
        tester = app.test_client(self)
        response = tester.post('/', 
            data=dict(delivery_date = "2022-03-12"))

    #tests delivery_date future (valid)
    def test_delivery_date_future_form(self):
        tester = app.test_client(self)
        response = tester.post('/', 
            data=dict(delivery_date = "2023-04-13"))

    #tests gallons (invalid) and delivery_date empty date (invalid)
    def test_both_empty_form(self):
        tester = app.test_client(self)
        response = tester.post('/', 
            data=dict(gallons = "", delivery_date = ""))

    #tests gallons negative (invalid) and delivery_date past date (invalid)
    def test_both_invalid_form(self):
        tester = app.test_client(self)
        response = tester.post('/', 
            data=dict(gallons = "-6", delivery_date = "2000-03-10"))

    #tests gallons zero (invalid) and delivery_date past date (invalid)
    def test_both_invalid_2_form(self):
        tester = app.test_client(self)
        response = tester.post('/', 
            data=dict(gallons = "0", delivery_date = "2000-03-09"))

    #tests gallons positive (valid) and delivery_date future date (valid)
    def test_both_valid_form(self):
        tester = app.test_client(self)
        response = tester.post('/', 
            data=dict(gallons = "9", delivery_date = "2055-03-15"))

    #tests gallons positive (valid) and delivery_date past date (invalid)
    def test_valid_invalid_form(self):
        tester = app.test_client(self)
        response = tester.post('/', 
            data=dict(gallons = "9", delivery_date = "1999-03-01"))

    #tests gallons zero (invalid) and delivery_date future date (valid)
    def test_invalid_valid_form(self):
        tester = app.test_client(self)
        response = tester.post('/', 
            data=dict(gallons = "0", delivery_date = "2222-05-05"))

    #tests gallons negative (invalid) and delivery_date future date (valid)
    def test_invalid_valid_2_form(self):
        tester = app.test_client(self)
        response = tester.post('/', 
            data=dict(gallons = "-999", delivery_date = "2223-01-01"))

if __name__ == '__main__':
    unittest.main()