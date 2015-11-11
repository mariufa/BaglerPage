
import psycopg2
import sys


class DbHelper:

    def __init__(self):
        self.databaseName = ''
        self.username = ''
        self.tableName = ''

    def loadCredidentials(self):

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
            data.append(People(row[0]), row[1], row[2])

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
            cur.execute("INSERT INTO " + self.tableName 
                    + " (Id, Name, Score) VALUES (%s, %s, %s)" 
                    % (person.idTag, person.name, person.score))
        con.commit()

        con.close()

class People:

    def __init__(self, idTag = 0, name = None, score = 0):
        self.name = name
        self.score = score
        self.idTag = idTag

con = None

try:
    con = psycopg2.connect(database='', user='')
    cur = con.cursor()
    
    cur.execute("DROP TABLE IF EXISTS Cars")
    cur.execute("CREATE TABLE Cars(Id INTEGER PRIMARY KEY, Name TEXT, Price INT)")
    cur.execute("INSERT INTO Cars VALUES(1, 'Audi', 52642)")
    cur.execute("INSERT INTO Cars VALUES(2, 'Mercedes', 57127)")
    cur.execute("INSERT INTO Cars VALUES(3, 'Skoda', 9000)")
    con.commit()
    
    cur.execute("SELECT * FROM Cars")
    rows = cur.fetchall()

    for row in rows:
        print row[1]

    #cur.execute("DROP TABLE IF EXISTS Cars")
    con.commit()
    cur.execute("CREATE TABLE IF NOT EXISTS Cars(Id INT PRIMARY KEY, Name TEXT, Price INT)")
    mycar = (4, "2", 3)
    query = "INSERT INTO Cars (Id, Name, Price) VALUES (%s, %s, %s)" % mycar
    cur.execute(query)
    con.commit()
    cur.execute("SELECT * FROM Cars")
    rows = cur.fetchall()
    print rows

    cur.execute("DROP TABLE IF EXISTS Cars")
    con.commit()


except psycopg2.DatabaseError, e:
    if con:
        con.rollback()

    print 'Error %s' % e
    sys.exit(1)

finally:
    if con:
        con.close()
        pass

