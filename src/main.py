from cws_heuristic import *

vehCap = 100.0 # update vehicle capacity for each instance
instanceName = 'A-n80-k10' # name of the instance
# txt file with the VRP instance data (nodeID, x, y, demand)
filename = 'data/' + instanceName + '_input_nodes.txt'
cws = CWS(filename)
cws.savings = multi_start_biased_randomized_algorithm(cws.savings)
solution = cws.run()
print(solution)