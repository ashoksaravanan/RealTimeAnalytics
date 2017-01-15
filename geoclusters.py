# To find hot-spots based on location data

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

#def find_hotspot(cluster_array):
    # finds top cluster


# main function

# copy latlong data
#csv_file = 'TwoClusterswithNoise.csv'
#df = pd.read_csv(csv_file)
#latArray = df['lat'].values
#lonArray = df['lon'].values
#locArray = np.array((latArray, lonArray)).T
#bookArray = df['booking'].values

conn_string = "host='localhost' dbname='gojek' user='postgres' password='karthi'"
conn = psycopg2.connect(conn_string)
curs = conn.cursor()

curs.execute("select ST_X(location),ST_Y(location) from gohack where service='ride' and isbooked='t';")
locArray = curs.fetchall()

#conn.close()

#print distance_matrix(locArray)

#print df

# clustering
#thresh = 0.05
thresh = 1.5
clusters = hcluster.fclusterdata(locArray, thresh, criterion="distance")
#clusters = hcluster.fclusterdata(distance_matrix(locArray), thresh, criterion="distance")
#df['cluster_id'] = clusters

#print clusters
#print df
cluster_ids = clusters.astype(np.int64)
np.savetxt('clusters.txt', cluster_ids)

# plotting
#x = np.arange(10)
#plt.scatter(*numpy.transpose(locArray), s=30, c=clusters)
#plt.axis("equal")
#title = "threshold: %f, number of clusters: %d" % (thresh, len(set(clusters)))
#plt.title(title)
#plt.show()


