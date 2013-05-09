import unittest

from google.appengine.api import users
from google.appengine.ext import db
from google.appengine.ext import testbed

from model import Group

class GroupTestCase(unittest.TestCase):

    def setUp(self):
        self.testbed = testbed.Testbed()
        self.testbed.activate()
        self.testbed.init_datastore_v3_stub()
        self.testbed.init_user_stub()

    def tearDown(self):
        self.testbed.deactivate()

    def test_insert_entity(self):
        Group(
            name = 'Mike Davis',
            owner = users.User(email='test@example.com', _user_id='1234567890')
            ).put()
        self.assertEqual(1, len(Group.all().fetch(2)))

if __name__ == '__main__':
    unittest.main()
