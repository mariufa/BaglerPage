import sys, os
# Enable import of classes from parent folder
sys.path.append('..')
import unittest
from baglerDbHelper import DbHelper, Person

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
        people = []
        people.append(Person(0, "Marius", 0))
        self.dbhelper.saveData(people)
        peopleLoaded = self.dbhelper.loadData()
        self.assertEqual(len(peopleLoaded), 1)
        person = peopleLoaded[0]
        self.assertEqual(person.idTag,0)
        self.assertEqual(person.name, "Marius")
        self.assertEqual(person.score, 0)


    def test_resetData(self):
        """
        Test to check if data table being emptied.
        """
        people = []
        people.append(Person(0, "Marius", 0))
        people.append(Person(1, "Marius2", 10))
        self.dbhelper.saveData(people)
        self.dbhelper.resetData()
        peopleLoaded = self.dbhelper.loadData()
        self.assertEqual(len(peopleLoaded), 0)

    def test_test(self):
        """
        Test to check test framework.
        """
        self.assertEqual(1,1)

    def tearDown(self):
        self.dbhelper.resetData()


if __name__ == "__main__":
    unittest.main()