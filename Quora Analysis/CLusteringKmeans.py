#############################################################################
# Full Imports

import math
import random
import csv

"""
This is a Python implementation of the K-Means Clustering algorithmn. The
original can be found here:
http://pandoricweb.tumblr.com/post/8646701677/python-implementation-of-the-k-means-clustering
"""

plotly = False
try:
    import plotly
    from plotly.graph_objs import Scatter, Scatter3d, Layout
except ImportError:
    print("INFO: Plotly is not installed, plots will not be generated.")

def main():
    dimensions = 3
    num_clusters = 2
    cutoff = 0.2
    points = []
    userPoints = {}
    pointUsers = {}
    with open('AverageValues.csv', 'r') as f:
        for row in f:
            line=row.split(",")
            line[3]=line[3].strip("\n")
            points.append(makeRandomPoint(float(line[1]),float(line[2]),float(line[3])))
            l = [float(line[1]), float(line[2]), float(line[3])]
            userPoints[line[0]] = l
            #pointUsers[float(line[1]), float(line[2]), float(line[3])] = line[0]
            #print(pointUsers)

    clusters = kmeans(points, num_clusters, cutoff)

    # Print our clusters
    for i, c in enumerate(clusters):
        for p in c.points:
            print(" Cluster: ", i, "\t Point :", p)
            q= str(p)
            with open('Users_Mapping(cluster_2).csv', 'a', newline='', encoding='UTF-8') as f:
                  fieldnames = ['userId', 'Cluster']
                  writer = csv.DictWriter(f, fieldnames=fieldnames)
                  #for k in userPoints.values():
                      #if str(k) == q:
                  writer.writerow({'userId':list(userPoints.keys())[p] , 'Cluster': i})

    # Display clusters using plotly for 2d data
    if dimensions in [2, 3] and plotly:
        print("Plotting points, launching browser ...")
        plotClusters(clusters, dimensions)

class Point(object):
    def __init__(self, coords):
        self.coords = coords
        self.n = len(coords)

    def __repr__(self):
        return str(self.coords)

class Cluster(object):
    def __init__(self, points):
        if len(points) == 0:
            raise Exception("ERROR: empty cluster")
        self.points = points
        self.n = points[0].n
        for p in points:
            if p.n != self.n:
                raise Exception("ERROR: inconsistent dimensions")
        self.centroid = self.calculateCentroid()

    def __repr__(self):
        return str(self.points)

    def update(self, points):
        old_centroid = self.centroid
        self.points = points
        self.centroid = self.calculateCentroid()
        shift = getDistance(old_centroid, self.centroid)
        return shift

    def calculateCentroid(self):
        numPoints = len(self.points)
        # Get a list of all coordinates in this cluster
        coords = [p.coords for p in self.points]
        # Reformat that so all x's are together, all y'z etc.
        unzipped = zip(*coords)
        # Calculate the mean for each dimension
        centroid_coords = [math.fsum(dList)/numPoints for dList in unzipped]

        return Point(centroid_coords)

def kmeans(points, k, cutoff):
    initial = random.sample(points, k)
    clusters = [Cluster([p]) for p in initial]

    loopCounter = 0
    while True:
        # Create a list of lists to hold the points in each cluster
        lists = [[] for _ in clusters]
        clusterCount = len(clusters)

        # Start counting loops
        loopCounter += 1
        # For every point in the dataset ...
        for p in points:
            smallest_distance = getDistance(p, clusters[0].centroid)
            clusterIndex = 0
            for i in range(clusterCount - 1):
                distance = getDistance(p, clusters[i+1].centroid)

                if distance < smallest_distance:
                    smallest_distance = distance
                    clusterIndex = i+1
            lists[clusterIndex].append(p)
        biggest_shift = 0.0
        for i in range(clusterCount):
            shift = clusters[i].update(lists[i])
            biggest_shift = max(biggest_shift, shift)
        if biggest_shift < cutoff:
            print("Converged after %s iterations" % loopCounter)
            break
    return clusters

def getDistance(a, b):
    if a.n != b.n:
        raise Exception("ERROR: non comparable points")

    accumulatedDifference = 0.0
    for i in range(a.n):
        squareDifference = pow((a.coords[i]-b.coords[i]), 2)
        accumulatedDifference += squareDifference
    distance = math.sqrt(accumulatedDifference)

    return distance

def makeRandomPoint(n, m,l):
    list=[n,m,l]
    p = Point(list)
    return p

def plotClusters(data, dimensions):
    if dimensions not in [2, 3]:
        raise Exception("Plots are only available for 2 and 3 dimensional data")

    # Convert data into plotly format.
    traceList = []
    for i, c in enumerate(data):
        # Get a list of x,y coordinates for the points in this cluster.
        cluster_data = []
        for point in c.points:
            cluster_data.append(point.coords)

        trace = {}
        centroid = {}
        if dimensions == 2:
            # Convert our list of x,y's into an x list and a y list.
            trace['x'], trace['y'] = zip(*cluster_data)
            trace['mode'] = 'markers'
            trace['marker'] = {}
            trace['marker']['symbol'] = i
            trace['marker']['size'] = 12
            trace['name'] = "Cluster " + str(i)
            traceList.append(Scatter(**trace))
            # Centroid (A trace of length 1)
            centroid['x'] = [c.centroid.coords[0]]
            centroid['y'] = [c.centroid.coords[1]]
            centroid['mode'] = 'markers'
            centroid['marker'] = {}
            centroid['marker']['symbol'] = i
            centroid['marker']['color'] = 'rgb(200,10,10)'
            centroid['name'] = "Centroid " + str(i)
            traceList.append(Scatter(**centroid))
        else:
            symbols = [
                "circle",
                "square",
                "diamond",
                "circle-open",
                "square-open",
                "diamond-open",
                "cross", "x"
            ]
            symbol_count = len(symbols)
            if i > symbol_count:
                print("Warning: Not enough marker symbols to go around")
            # Convert our list of x,y,z's separate lists.
            trace['x'], trace['y'], trace['z'] = zip(*cluster_data)
            trace['mode'] = 'markers'
            trace['marker'] = {}
            trace['marker']['symbol'] = symbols[i]
            trace['marker']['size'] = 12
            trace['name'] = "Cluster " + str(i)
            traceList.append(Scatter3d(**trace))
            # Centroid (A trace of length 1)
            centroid['x'] = [c.centroid.coords[0]]
            centroid['y'] = [c.centroid.coords[1]]
            centroid['z'] = [c.centroid.coords[2]]
            centroid['mode'] = 'markers'
            centroid['marker'] = {}
            centroid['marker']['symbol'] = symbols[i]
            centroid['marker']['color'] = 'rgb(200,10,10)'
            centroid['name'] = "Centroid " + str(i)
            traceList.append(Scatter3d(**centroid))

    title = "K-means clustering with %s clusters" % str(len(data))
    plotly.offline.plot({
        "data": traceList,
        "layout": Layout(title=title)
    })

if __name__ == "__main__":
    main()