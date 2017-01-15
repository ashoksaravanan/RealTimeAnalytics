#!/usr/bin/python
import psycopg2
import sys
import pprint

conn_string = "host='localhost' dbname='gojek' user='postgres' password='karthi'"
conn = psycopg2.connect(conn_string)
cursor = conn.cursor()

 
def main():
    #conn_string = "host='localhost' dbname='gojek' user='postgres' password='karthi'"
    #print "Connecting to database\n ->%s" % (conn_string)
    #conn = psycopg2.connect(conn_string)
    #global cursor = conn.cursor()	
    cursor.execute("select count(*) from gohack where service='"+str(sys.argv[1])+"';")
    records = cursor.fetchone()
    print("No of users in last 24 hours: ",str(records[0]))

def last_30minutes():
    cursor.execute("select count(*) from gohack as g where service='"+str(sys.argv[1])+"' and  g.loggedtime > current_timestamp -interval '30 minutes';")
    last30mins = cursor.fetchone()
    print("No of users in last 30 mins:", str(last30mins[0]))
 
if __name__ == "__main__":
    main()
    last_30minutes()
