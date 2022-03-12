from loginBackend import app
import unittest


class FlaskTestCase(unittest.TestCase):

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

    #ensure login behaves correctly given valid field inputs
    def test_correct_form(self):
        tester = app.test_client(self)
        response = tester.post('/',
            data=dict(username= "root",
                    password= '123456'
                ))
        self.assertTrue(b'Login Successful' in response.data)
    
    #ensure login behaves correctly given invalid field inputs
    def test_incorrect_form(self):
        tester = app.test_client(self)
        response = tester.post('/',
            data=dict(username= "root",
                    password= '126'
                ))
        self.assertTrue(b'User not found' in response.data)

if __name__ == '__main__':
    unittest.main()