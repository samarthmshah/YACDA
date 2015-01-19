__author__ = 'SAMARTH'

import os
import utilities

filepath = os.path.join(".", "..", "DATA", "facebook.txt")
edgeSet = set()

edgesTS, sorted_nodes, edges, new_nodeDictionary, number_days, total_ids = utilities.readFile(filepath)

#UPDATING edgesTS
edgesTS = utilities.updateEdgesTS(edgesTS, new_nodeDictionary)

#adding all the edges in edgeTS into edgeSet.
for i in range(len(edgesTS)):
    edgeSet.add(tuple([edgesTS[i][1][0],edgesTS[i][1][1]]))

#now, adding all the edges between the same nodes at different time (days)

for i in range(len(sorted_nodes)):
    edgeSet.add(tuple([sorted_nodes[i], new_nodeDictionary[0][sorted_nodes[i]]]))

for i in range(1, number_days):
    for j in range(0, len(sorted_nodes)):
        edgeSet.add(tuple([new_nodeDictionary[i-1][sorted_nodes[j]], new_nodeDictionary[i][sorted_nodes[j]]]))

edgeList = list(edgeSet)
# print edgeList

#neighborhoodRecord is a dictionary with the temporal neighborhood of each node!!!!
neighborhoodRecord = utilities.temporalNeighborhood(edgeList, total_ids)

# =========================================================================================
# Cannot print the entire neighborhoodRecord dictionary since it is too much to process.
# We can check the neighborhood set of a node by putting the node value in the statement below
# =========================================================================================
print 'Example: The neighborhood set of 0 is ', neighborhoodRecord[0]
# =========================================================================================
#If we put 0 -> 4117 will be in the neighborhoodRecord[0]...1 will have 4118 =====
# This shows chaining in the temporal ids.
# =========================================================================================

#hash them..