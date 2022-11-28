import sys
sys.path.insert(0, '../src')
from cws.cws_heuristic import *
from unittest import mock

def test_cws():
    
    instances = [
        (100, "A-n80-k10", 1860.94), 
        (100, "B-n57-k9", 1653.42),
        (6000, "E-n22-k4", 388.77),
        (2010, "F-n45-k4", 739.02),
        (200, "M-n101-k10", 833.51),
        (135, "P-n70-k10", 896.86)
     ]

    for instance in instances:
        vehicle_capacity = instance[0]
        instance_name = instance[1]
        expected_cost = instance[2]

        filename = 'data/' + instance_name + '_input_nodes.txt'
        cws = CWS(filename, vehicle_capacity=vehicle_capacity)
        solution = cws.run()
        assert len(cws.savings) == 0
        assert float("{:.2f}".format(solution.cost)) == expected_cost