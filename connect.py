#!/usr/bin/python
import psycopg2
import sys
import random
import pprint
from random import randint 

def main():
    conn_string = "host='localhost' dbname='gojek' user='postgres' password='karthi'"
    #print "Connecting to database\n ->%s" % (conn_string)
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()

    #services = ["ride", "car", "food", "mart", "send", "glam", "tix", "massage", "auto", "pulsa"]
    services=["ride","glam","car","food"]
    y=int(sys.argv[3])
    for x in range(0,y):
    	mypoint1 = "("+ str(randint(1,25000))+ ",ST_MakePoint("+sys.argv[1]+"."+str(randint(10,99))+str(randint(10,99))+","+str(sys.argv[2])+"."+ str(randint(10, 99)) + str(randint(10, 99))+")"
    	mypoint2 = mypoint1 + ",'"+ str(services[randint(0,3)])+"',"+str(random.choice([True, False])) + ");"
    	query = "insert into gohack(userid, location, service, isbooked) values"+str(mypoint2).strip(' \t\n\r')    
	cursor.execute(str(query))

    conn.commit()
    #records = cursor.fetchall()
    #pprint.pprint(records)
    #print(cursor.fetchone()[0])
 
if __name__ == "__main__":
    main()
