import sys, os
sys.path.append('..')
import unittest
from baglerDbHelper import DbHelper

class DatabaseTestCase(unittest.TestCase):

    def setUp(self):
        pass


    def test_loadCredidentials(self):
        """
        Test to check loading of credidentials.
        """
        dbhelper = DbHelper()
        dbhelper.loadCredidentials()
        self.assertGreater(len(dbhelper.username), 0)
        self.assertGreater(len(dbhelper.databaseName), 0)
        self.assertGreater(len(dbhelper.tableName), 0)

    def test_loadCredidentialsNotLoaded(self):
        """
        Test to check not loading of credidentials.
        """
        dbhelper = DbHelper()
        self.assertEqual(len(dbhelper.username), 0)
        self.assertEqual(len(dbhelper.databaseName), 0)
        self.assertEqual(len(dbhelper.tableName), 0)

    def test_test(self):
        """
        Test to check test framework.
        """
        self.assertEqual(1,1)


if __name__ == "__main__":
    unittest.main()