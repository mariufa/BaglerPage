
import psycopg2
import sys, os


class DbHelper:
    """
    3 functions to use are loadCredentials, loadData and saveData.
    """

    def __init__(self):
        self.credentials = Credentials()

    def loadCredentials(self):
        """
        Loads settings from file.
        """
        self.credentials.loadCredentials()
        
    def loadData(self):
        """
        Reads person info and stores it in a list of Person objects.

        Args:

        Returns:
            A list of Person objects.
        """
        con = None
        con = psycopg2.connect(database = self.credentials.databaseName, user = self.credentials.username)
        cur = con.cursor()

        # In case table does not exists already
        self.setupTable(cur)
        # Save changes
        con.commit()

        # Read from table.
        cur.execute("SELECT * FROM " + self.credentials.tableName)

        # Get all rows from database table.
        rows = cur.fetchall()
        data = self.tranformFromTableToList(rows)# Close connection

        # Close connection.
        con.close()
        return data

    def tranformFromTableToList(self, rows):
        data = []
        for row in rows:
            data.append(Person(row[0], row[1], row[2]))

        return data

    def saveData(self, data):
        """
        Writes over current table with new data.

        Args:
            data: List of Person objects to be stored in table.
        """
        con = None
        con = psycopg2.connect(database = self.credentials.databaseName , user = self.credentials.username)
        cur = con.cursor()

        self.resetTable(cur)
        self.insertIntoTable(cur, data)
        # Save changes
        con.commit()
        # Close connection
        con.close()

    def insertIntoTable(self, cur, data):
        """
        Inserts data into database table.

        Args:
            cur: Cursor in table
            data: List of persons.
        """
        for person in data:
            query = "INSERT INTO " + self.credentials.tableName + " (Id, Name, Score) VALUES (%s, %s, %s)"
            cur.execute(query, (person.idTag, person.name, person.score))

    def resetTable(self, cur):
        """
        Deletes table and recreates it.

        Args:
            cur: Cursor of table
        """
        self.deleteTable(cur)
        self.setupTable(cur)

    def deleteTable(self, cur):
        """
        Deletes table.

        Args:
            cur: Cursor of table
        """
        cur.execute("DROP TABLE IF EXISTS " + self.credentials.tableName)

    def setupTable(self, cur):
        """
        Creates table.

        Args:
            cur: Cursor of table
        """
        cur.execute("CREATE TABLE IF NOT EXISTS "
                    + self.credentials.tableName
                    + "(Id INTEGER PRIMARY KEY, Name TEXT, Score INT)")

    def getTableName(self):
        return self.credentials.tableName

    def getDatabaseName(self):
        return self.credentials.databaseName

    def getUsername(self):
        return self.credentials.username

    def resetData(self):
        """
        Deletes data in table
        """
        self.saveData([])



class Person:

    def __init__(self, idTag = 0, name = None, score = 0):
        """
        Constructor.

        Args:
            idTag: Int number.
            name: Text string
            score: Int number
        """
        self.name = name
        self.score = score
        self.idTag = idTag

class Credentials:

    def __init__(self):
        self.databaseName = ''
        self.username = ''
        self.tableName = ''
        self.fileName = "credentials.txt"

    def loadCredentials(self):
        """
        Loads names from file.
        """
        location = self.getFilePathOfScript()
        fileCred = open(os.path.join(location,self.fileName), "r")
        for line in fileCred:
            # Remove spaces, new lines and split in two where ':'.
            line = line.strip().split(":")
            if line[0] == "user":
                self.username = line[1]
            elif line[0] == "db":
                self.databaseName = line[1]
            elif line[0] == "table":
                self.tableName = line[1]
        fileCred.close()

    def getFilePathOfScript(self):
        """
        Used to make sure of location of credentials.txt.

        Returns:
            File location. String.
        """
        return os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))