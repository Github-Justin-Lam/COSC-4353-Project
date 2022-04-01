from historyBackend import app
import unittest

"""
Name                Stmts   Miss  Cover   Missing
-------------------------------------------------
historyBackend.py      23      0   100%
historyTest.py         14      0   100%
-------------------------------------------------
TOTAL                  37      0   100%
"""

class FlaskTestCase(unittest.TestCase):

    #ensure that flask was set up correctly
    def test_index(self):
        tester = app.test_client(self)
        response = tester.get('/', content_type='html/text')
        self.assertEqual(response.status_code, 200) #request is successful

    #ensure that page loaded correctly
    def test_history_loads(self):
        tester = app.test_client(self)
        response = tester.get('/', content_type='html/text')
        self.assertTrue(b'Fuel Quote History' in response.data)

if __name__ == '__main__':
    unittest.main()