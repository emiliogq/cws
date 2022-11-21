import sys
sys.path.insert(0, '../src')
from cws_heuristic import *

def test_basic_cws():
    vehCap = 100.0 # update vehicle capacity for each instance
    instanceName = 'A-n80-k10' # name of the instance
    # txt file with the VRP instance data (nodeID, x, y, demand)
    filename = 'data/' + instanceName + '_input_nodes.txt'
    cws = CWS(filename)
    solution = cws.run()
    assert solution.cost == 1860.9424980238105

def test_multistart_biased_randomized_cws():
    vehCap = 100.0 # update vehicle capacity for each instance
    instanceName = 'A-n80-k10' # name of the instance
    # txt file with the VRP instance data (nodeID, x, y, demand)
    filename = 'data/' + instanceName + '_input_nodes.txt'
    cws = CWS(filename)
    cws.savings = multi_start_biased_randomized_algorithm(cws.savings)
    solution = cws.run()
    assert len(cws.savings) == 0
