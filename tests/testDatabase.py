import sys, os
# Enable import of classes from parent folder
sys.path.append('..')
import unittest
from baglerDbHelper import DbHelper, People

class DatabaseTestCase(unittest.TestCase):

    def setUp(self):
        self.dbhelper = DbHelper()
        self.dbhelper.loadCredentials()

    def test_loadCredentials(self):
        """
        Test to check loading of credentials.
        """
        self.assertGreater(len(self.dbhelper.username), 0)
        self.assertGreater(len(self.dbhelper.databaseName), 0)
        self.assertGreater(len(self.dbhelper.tableName), 0)


    def test_LoadAndSaveData(self):
        """
        Test to check loading and saving of data
        """
        peoples = []
        peoples.append(People(0, "Marius", 0))
        self.dbhelper.saveData(peoples)
        peoplesLoaded = self.dbhelper.loadData()
        self.assertEqual(len(peoplesLoaded), 1)
        people = peoplesLoaded[0]
        self.assertEqual(people.idTag,0)
        self.assertEqual(people.name, "Marius")
        self.assertEqual(people.score, 0)


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