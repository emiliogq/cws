from cws.cws_heuristic import *
from operator import attrgetter

def multi_start_biased_randomized_algorithm(filename: str, vehicle_capacity=100, iterations = 10, beta = 0.3) -> Solution:
    solutions = []
    while (iterations > 0):
        cws = CWS(filename, vehicle_capacity)
        cws.savings_from_geometric(beta)
        solution = cws.run()
        solutions.append(solution)
        iterations -= 1
    return min(solutions, key=attrgetter('cost'))