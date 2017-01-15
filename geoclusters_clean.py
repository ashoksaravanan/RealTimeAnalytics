# To find hot-spots based on location data

import sys
import psycopg2
import numpy as np
import scipy.cluster.hierarchy as hcluster
from math import cos, asin, sqrt

# functions

def distance(loc1, loc2):
    # compute distance between 2 lat-long co-ordinates using Haversine formula
    lat1 = loc1[0]
    lon1 = loc1[1]
    lat2 = loc2[0]
    lon2 = loc2[1]
    p = 0.017453292519943295
    a = 0.5 - cos((lat2 - lat1) * p)/2 + cos(lat1 * p) * cos(lat2 * p) * (1 - cos((lon2 - lon1) * p)) / 2
    return 12742 * asin(sqrt(a))

def distance_matrix(loc_array):
    # compute distance between 2 arrays of lat-long co-ordinates & returns square matrix
    dis_matrix = np.empty([len(loc_array), len(loc_array)], dtype=float)

    for i in xrange(len(loc_array)):
        for j in xrange(len(loc_array)):
            dis_matrix[i][j] = distance(loc_array[i],loc_array[j])
    return dis_matrix

def centeroidnp(arr):
    # find centeroid of polygon
    length = arr.shape[0]
    sum_x = np.sum(arr[:, 0])
    sum_y = np.sum(arr[:, 1])
    return sum_x/length, sum_y/length

def poly_edges(points):
    # find 4 edges of polygon
    north = points[np.argmax(points[:,1])]
    east = points[np.argmax(points[:,0])]
    south = points[np.argmin(points[:,1])]
    west = points[np.argmin(points[:,0])]
    return (north, east, south, west)

# main function

conn_string = "host='localhost' dbname='gojek' user='postgres' password='karthi'"
conn = psycopg2.connect(conn_string)
curs = conn.cursor()
curs.execute("select ST_X(location),ST_Y(location) from gohack as g where service='"+sys.argv[1]+"' and isbooked='t' and  g.loggedtime > current_timestamp -interval '30 minutes';")
locArray = curs.fetchall()

thresh = 0.005
clusters = np.array(hcluster.fclusterdata(locArray, thresh, criterion="distance"), dtype=int)
hotspot = np.bincount(clusters).argmax()
indices = [i for i, j in enumerate(clusters) if j == hotspot]

hotspot_points = np.array([locArray[i] for i in indices])
print "Current demand in hotspot: ", len(hotspot_points)

centeroid = centeroidnp(hotspot_points)
print "Centeroid of hotspot: ", centeroid

edges = poly_edges(hotspot_points)
print "Edges of hotspot: ", edges
