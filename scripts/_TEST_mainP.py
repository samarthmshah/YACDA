__author__ = 'SAMARTH'

import os
import utilities as util

filepath = os.path.join(".", "..", "DATA", "facebook.txt")
edgeSet = set()

edgesTS, number_days, number_nodes, trial_new_node_dict = util.readFile(filepath)

#UPDATING edgesTS
# OLD call
# edgesTS = util.updateEdgesTS(edgesTS, new_nodeDictionary, number_nodes, trial_new_node_ids, trial_new_node_dict)
# NEW call
edgesTS = util.updateEdgesTS(edgesTS, number_nodes, trial_new_node_dict)

##++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
##++++++++++++++++++      NEW CODE STARTS HERE     ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#N is the hash table (Dictionary) which stores the neighborhoods of all the nodes.
N = {}
# d = no. of hops+++++ j and _j are iterators.
d = 1
j = 1
_j = 1

for i in range(number_nodes):
    for t in range(number_days):
        index = (t * number_nodes) + i
        #adding the node itself
        N[index] = [index]
        #computes neighborhood in a SINGLE time-slice
        N[index] += util.neigh(t, index, d, edgesTS)
        # Computing neighborhood in previous time
        while j <= d and t-j >= 0:
            N[index] += util.neigh(t-j, index, d-j, edgesTS)
            j += 1
        # Computing neighborhood in subsequent time
        while _j <= d and t+_j < number_days:
            N[index] += util.neigh(t+_j, index, d-_j, edgesTS)
            _j += 1

# print 'The Neighborhood Hash-Table / Dictionary is  ' ,N

##++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
##++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


##++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
##++++++++++++++++++      OLD CODE STARTS HERE     ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#adding all the edges in edgeTS into edgeSet.
# for i in range(len(edgesTS)):
#     edgeSet.add(tuple([edgesTS[i][1][0],edgesTS[i][1][1]]))
#
# #now, adding all the edges between the same nodes at different time (days)
#
# for i in range(len(sorted_nodes)):
#     edgeSet.add(tuple([sorted_nodes[i], new_nodeDictionary[0][sorted_nodes[i]]]))
#
# for i in range(1, number_days):
#     for j in range(0, len(sorted_nodes)):
#         edgeSet.add(tuple([new_nodeDictionary[i-1][sorted_nodes[j]], new_nodeDictionary[i][sorted_nodes[j]]]))
#
# edgeList = list(edgeSet)
# # print edgeList
#
# #neighborhoodRecord is a dictionary with the temporal neighborhood of each node!!!!
# # neighborhoodRecord = utilities.temporalNeighborhood(edgeList, total_ids)
#
# # =========================================================================================
# # Cannot print the entire neighborhoodRecord dictionary since it is too much to process.
# # We can check the neighborhood set of a node by putting the node value in the statement below
# # =========================================================================================
# # print 'Example: The neighborhood set of 0 is ', neighborhoodRecord[0]
# # =========================================================================================
# #If we put 0 -> 4117 will be in the neighborhoodRecord[0]...1 will have 4118 =====
# # This shows chaining in the temporal ids.
# # =========================================================================================
#
# #hash them..