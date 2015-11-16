from baglerDbHelper import DbHelper

def clearTableInDb():
    dbhelper = DbHelper()
    dbhelper.loadCredentials()
    dbhelper.resetData()

if __name__ == "__main__":
    clearTableInDb()