# To target new go-glam users based on location data

import sys
import psycopg2
import numpy as np

# main function

conn_string = "host='localhost' dbname='gojek' user='postgres' password='karthi'"
conn = psycopg2.connect(conn_string)
curs = conn.cursor()

# Query 1

query1 = "SELECT ST_MakePolygon(ST_AddPoint(foo.open_line, ST_StartPoint(foo.open_line))) FROM (SELECT ST_GeomFromText('LINESTRING("+sys.argv[1]+" "+sys.argv[2]+","+sys.argv[3]+" "+sys.argv[4]+","+sys.argv[5]+" "+sys.argv[6]+","+sys.argv[7]+" "+sys.argv[8]+")') As open_line) As foo;"

curs.execute(query1)
geopol = curs.fetchall()
geopol = str(geopol[0][0])
print geopol

# Query 2

query2 ="select count(*) from gohack as g where ST_Contains(ST_AsText('"+geopol+"'), g.location);"
print query2
curs.execute(query2)
totalUsers = curs.fetchall()
totalUsers = int(totalUsers[0][0])
print totalUsers

# Query 3

query3 = "select count(*) from gohack as g where ST_Contains(ST_AsText('" + geopol+ "'), g.location) and st_area('" + geopol+ "') < 0.05 and g.service='glam'  GROUP BY service;"
curs.execute(query3)
glamUsers = curs.fetchall()
glamUsers = int(glamUsers[0][0])
print glamUsers

# Query 4
print 13/float(100)
print  (13/float(100))*totalUsers

if( (15/float(100))*totalUsers >= glamUsers ):
    query4 = "select distinct(userid) from gohack as g where ST_Contains(ST_AsText('" + geopol + "'), g.location) and g.service <> 'glam';"
    curs.execute(query4)
    target_users = curs.fetchall()
    print np.array([target_users[i] for i in len(target_users)])
else:
    print "Number of Go-glam users is less than 5% in hotspot"
