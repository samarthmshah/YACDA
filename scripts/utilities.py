__author__ = 'SAMARTH'

import networkx as nx

def readFile(filepath):

    # edgesTS stores edges along with the time. (__day__)
    edgesTS = []
    nodes = set()
    edges = set()

    #=========================================================================================================
    #===new node_Dict's will keep a record of the "link" from the same node at different time instances.======
    #=========================================================================================================
    new_nodeDict = {}
    new_nodeDict2 = {}
    new_nodeDict3 = {}
    new_nodeDict4 = {}
    new_nodeDict5 = {}
    new_nodeDict6 = {}

    # ================to open the file facebook.txt
    with open(filepath,'r') as fd:
        for line in fd.readlines():

            #A line would look something like this ---->"2006-05-09 04:10:57" 12830 14791<---

            #==================================================================================
            #======PREPROCESING================================================================
            line = line.strip()
            items = line.split(' ')
            #put every word in item list

            #take first two words as timestamps.
            tstamp = ' '.join(items[0:2])
            #avoiding '"' here.
            tstamp = tstamp[1:-1]

            # As the year is 2006 in the entire dataset, we don't care about 2006 anymore! we just take the month-day.
            timestamp = tstamp[5:10]

            #tstamp = datetime.strptime(tstamp, '%Y-%m-%d %H:%M:%S')
            #formatting it into this form %Y-%m-%d %H:%M:%S

            timemonth = int(timestamp[0:2])
            timeday = int(timestamp[3:5])
            #timestamp = ' '.join(timestamp[0:2])

            #The first entry 05-09 should be day 0. 06-09 should be day 1, and so on.
            if timemonth == 5:
                day = timeday - 9
            elif timemonth == 6:
                day = timeday + 23
            elif timemonth == 7:
                day = timeday + 53
            elif timemonth == 8:
                day = timeday + 84

            #t will be the id of the two nodes.
            t = items[2:4]

            t = map(int,t)

            if t[0] == t[1]:
                continue
            t.sort(); #undirected..small ID first

            edgesTS.append((day, t))
            nodes.add(t[0])
            nodes.add(t[1])
            edges.add(tuple([t[0],t[1]]))

    #node_list will contain all the nodes having edges
    #sorted_nodes will contain all the nodes having edges in sorted order.
    #new_nodeDict will be just a mapping of the form {new_id : old_id}
    node_list = list(nodes)
    sorted_nodes = sorted(node_list)
    number_nodes = len(node_list)
    number_days = edgesTS[len(edgesTS) - 1][0] + 1
    total_ids = number_days * number_nodes

    print 'Total number of nodes in the dataset are: ', number_nodes
    print 'Total number of days in the dataset are: ', number_days
    print 'Therefore, total number of newly generated temporal ids will be: ', total_ids
    # print 'node_list in a sorted order is: ',sorted_nodes # <-- This statement takes too much processing.

    #temporal_id_keeper is a list of lists containing 105 lists of 4117 numbers (in succession) each.
    #temporal_id_keeper[0] will have all the numbers from 0 to 4117 - depicting the node id at time 0.
    #temporal_id_keeper[x] will have all the numbers which depict the node_id at time x.
    temporal_id_keeper = [range(number_nodes * i, number_nodes * (i+1)) for i in range(0, number_days)]

    # new_nodeDictionary keeps track of the same node at different times.
    # node 0 at time 0 will be linked with node 4118. 4118 will be linked with 8235, and so on.
    # It will be used to add the edges between nodes at time t+1 and t-1.
    new_nodeDictionary = {}
    for i in range(0, number_days):
        new_nodeDictionary[i] = dict(zip(sorted_nodes, temporal_id_keeper[i]))

    # print 'Old edgeTS is ',edgesTS
    fd.close()

    return edgesTS, sorted_nodes, edges, new_nodeDictionary, number_days, total_ids

# def classicNeighborhood(edges, nodes):
#     normal_neighborhood = {}
#     neighborIndividual = []
#
#     for node in nodes:
#         normal_neighborhood[node] = None
#         for edge in edges:
#             if edge[0] == node:
#   #              normal_neighborhood[node] = edge[1]
#                 neighborIndividual.append(edge[1])
#             elif edge[1] == node:
# #                normal_neighborhood[node] = edge[0]
#                 neighborIndividual.append(edge[0])
#             else:continue
#             #print neighborIndividual
#         normal_neighborhood[node] = neighborIndividual
#         del neighborIndividual[:]
#
#     #normal_neighborhood[node] = neighborIndividual
#     return normal_neighborhood

def updateEdgesTS (edgesTS, new_nodeDictionary):

    # replace the node_id with temporal_id first. So all nodes will have new IDs now.
    for i in range(len(edgesTS)):
        x = edgesTS[i][0]; # =========== x is the day
        edgesTS[i][1][0] = new_nodeDictionary[x][edgesTS[i][1][0]]
        edgesTS[i][1][1] = new_nodeDictionary[x][edgesTS[i][1][1]]

    # print 'updated edgeTS : ', edgesTS
    return edgesTS

def temporalNeighborhood(edgeList, total_ids):
    neighborhoodRecord = {}
    G = nx.Graph()
    G.add_edges_from(edgeList)

    for i in range(0, total_ids):
        neighborhoodRecord[i] = G.neighbors(i)

    # print 'Neighbors of keys are all the values ',neighborhoodRecord
    return neighborhoodRecord