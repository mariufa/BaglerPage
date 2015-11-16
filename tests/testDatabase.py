import sys, os
# Enable import of classes from parent folder
sys.path.append('..')
import unittest
from baglerDbHelper import DbHelper, People

class DatabaseTestCase(unittest.TestCase):

    def setUp(self):
        pass


    def test_loadCredentials(self):
        """
        Test to check loading of credentials.
        """
        dbhelper = DbHelper()
        dbhelper.loadCredentials()
        self.assertGreater(len(dbhelper.username), 0)
        self.assertGreater(len(dbhelper.databaseName), 0)
        self.assertGreater(len(dbhelper.tableName), 0)

    def test_loadCredentialsNotLoaded(self):
        """
        Test to check not loading of credentials.
        """
        dbhelper = DbHelper()
        self.assertEqual(len(dbhelper.username), 0)
        self.assertEqual(len(dbhelper.databaseName), 0)
        self.assertEqual(len(dbhelper.tableName), 0)

    def test_LoadAndSaveData(self):
        """
        Test to check loading and saving of data
        """
        dbhelper = DbHelper()
        dbhelper.loadCredentials()
        peoples = []
        peoples.append(People())

        pass

    def test_resetData(self):
        """
        Test to check if data table being emptied.
        """
        pass

    def test_test(self):
        """
        Test to check test framework.
        """
        self.assertEqual(1,1)

    def tearDown(self):
        pass


if __name__ == "__main__":
    unittest.main()