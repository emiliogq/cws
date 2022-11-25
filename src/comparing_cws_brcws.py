from cws_heuristic import *
from multistart_brcws import *

instances = [
    (100, "A-n80-k10", 1860.94), 
    (100, "B-n57-k9", 1653.42),
    (6000, "E-n22-k4", 388.77),
    (2010, "F-n45-k4", 739.02),
    (200, "M-n101-k10", 833.51),
    (135, "P-n70-k10", 896.86)
]
results = []
for instance in instances :
    vehicle_capacity = instance[0]
    instance_name = instance[1]
    filename = 'data/' + instance_name + '_input_nodes.txt'
    runners = [ 
        ("cws", CWS(filename, vehicle_capacity).run()), 
        ("br-cws", multi_start_biased_randomized_algorithm(filename, vehicle_capacity, iterations=1000, beta=0.4))
    ]
    for runner in runners:
        runner_name = runner[0]
        solution = runner[1]
        print(instance_name + "," + runner_name + "," + "{:.{}f}".format(solution.cost,2))