
import psycopg2
import sys, os


class DbHelper:

    def __init__(self):
        self.databaseName = ''
        self.username = ''
        self.tableName = ''
        self.fileName = "credentials.txt"

    def loadCredentials(self):
        """
        Loads settings from file.
        """
        location = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
        fileCred = open(os.path.join(location,self.fileName), "r")
        for line in fileCred:
            line = line.strip().split(":")
            if line[0] == "user":
                self.username = line[1]
            elif line[0] == "db":
                self.databaseName = line[1]
            elif line[0] == "table":
                self.tableName = line[1]
        fileCred.close()
        
    def loadData(self):
        """
        Reads person info and stores it in a list of Person objects.

        Args:

        Returns:
            A list of Person objects.
        """
        con = None
        con = psycopg2.connect(database = self.databaseName, user = self.username)
        cur = con.cursor()

        # In case table does not exists already
        cur.execute("CREATE TABLE IF NOT EXISTS " 
                + self.tableName 
                + "(Id INT PRIMARY KEY, Name TEXT, Score INT)")
        con.commit()

        cur.execute("SELECT * FROM " + self.tableName)
        data = []
        rows = cur.fetchall()
        for row in rows:
            data.append(People(row[0], row[1], row[2]))

        con.close()
        return data

    def saveData(self, data):
        """
        Writes over current table with new data.

        Args:
            data: List of Person objects to be stored in table.

        Returns:
            Nothing.
        """
        con = None
        con = psycopg2.connect(database = self.databaseName , user = self.username)
        cur = con.cursor()

        cur.execute("DROP TABLE IF EXISTS " + self.tableName)
        cur.execute("CREATE TABLE " 
                + self.tableName 
                + "(Id INTEGER PRIMARY KEY, Name TEXT, Score INT)")

        for person in data:
            query ="INSERT INTO " + self.tableName + " (Id, Name, Score) VALUES (%s, %s, %s)"
            cur.execute(query, (person.idTag, person.name, person.score))

        con.commit()

        con.close()

    def resetData(self):
        """
        Deletes data in table

        """
        self.saveData([])



class People:

    def __init__(self, idTag = 0, name = None, score = 0):
        """
        Constructor

        Args:
            idTag: Int number.
            name: Text string
            score: Int number

        Returns:

        """
        self.name = name
        self.score = score
        self.idTag = idTag


