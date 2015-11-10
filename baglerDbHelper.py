
import psycopg2
import sys


con = None

try:
    con = psycopg2.connect(database='baglerdb', user='mariufa')
    cur = con.cursor()
    cur.execute('SELECT version()')
    ver = cur.fetchone()
    print ver
    print "yes"

except psycopg2.DatabaseError, e:
    print 'Error %s' % e
    sys.exit(1)

finally:
    if con:
        con.close()
