import sys
sys.path.insert(0, '../src')
from cws_heuristic import *
from unittest import mock

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
    mocked_random_choice = lambda : 0.5
    with mock.patch('random.random', mocked_random_choice):
        cws.savings = multi_start_biased_randomized_algorithm(cws.savings)
    solution = cws.run()
    assert len(cws.savings) == 0
    assert solution.cost == 1872.98102431723
