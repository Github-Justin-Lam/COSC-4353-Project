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

    #ensure registration behaves correctly given valid field inputs
    def test_correct_form(self):
        tester = app.test_client(self)
        response = tester.post('/register',
            data=dict(email="username@gmail.com",
                    username= "root",
                    password= "123456"
                ))
        self.assertTrue(b'You are now registered and can log in' in response.data)

    #ensure login behaves correctly given valid field inputs
    """def test_correct_form(self):
        tester = app.test_client(self)
        response = tester.post('/login',
            data=dict(username= "root",
                    password= '123456'
                ))
        self.assertTrue(b'Login Successful' in response.data)"""
    
    #ensure login behaves correctly given invalid field inputs
    def test_incorrect_form(self):
        tester = app.test_client(self)
        response = tester.get('/login',
            data=dict(username= "root",
                    password= '126'
                ))
        self.assertTrue(b'Username not found' in response.data)

if __name__ == '__main__':
    unittest.main()