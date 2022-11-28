from vrp.nodes.node import Node
from vrp.edges.edge import Edge 
from vrp.routes.route import Route
from vrp.solutions.solution import Solution

import math, random
import operator


class CWS :

    def __init__(self, filename, vehicle_capacity = 100) -> None:
        self.vehicle_capacity = vehicle_capacity
        self.depot, self.destinations = self.read_nodes(filename)
        self.create_destination_edges()
        self.solution = Solution(self.destinations)
        self.savings = []
        self.init_savings()
    
    def read_nodes(self, filename: str):
        with open(filename) as instance:
            i = 0
            nodes = []
            for line in instance:
                # array data with node data: x, y demand
                data = [float(x) for x in line.split()]
                aNode = Node(i, data[0], data[1], data[2])
                nodes.append(aNode)
                i += 1
        depot = nodes[0] # node 0 is depot
        destinations = nodes[1:]
        return depot, destinations
        
    def init_savings(self):
        for i in range(len(self.destinations)):
            destination_a = self.destinations[i]
            for j in range(i+1, len(self.destinations)):
                destination_b = self.destinations[j]
                ijEdge = Edge(destination_a, destination_b) # creates the (i, j) edge
                jiEdge = Edge(destination_b, destination_a)
                ijEdge.inverse_edge = jiEdge # sets the inverse edge
                jiEdge.inverse_edge = ijEdge
                # compute the Euclidean distance as cost
                ijEdge.cost = math.sqrt((destination_b.x - destination_a.x)**2 + (destination_b.y - destination_a.y)**2)
                jiEdge.cost = ijEdge.cost # assume symmectir costs
                # compute savins as proposed by Clark & Wright
                ijEdge.savings = destination_a.to_depot_edge.cost + destination_b.from_depot_edge.cost - ijEdge.cost
                jiEdge.savings = ijEdge.savings
                # save one edge in the savings list
                self.savings.append(ijEdge)
        self.savings.sort(key = operator.attrgetter("savings"), reverse = True)

    def savings_from_geometric(self, beta = 0.3):
        savings_copy = self.savings.copy()
        end_list = []
        while(len(savings_copy) > 0):
            index = int(math.log(random.random()) / math.log(1 - beta))
            index = index % len(savings_copy)
            end_list.append(savings_copy[index])
            savings_copy.pop(index)
        self.savings = end_list

    def create_destination_edges(self):
        for node in self.destinations:
            dnEdge = Edge(self.depot, node) # creates (depot, node) edge
            ndEdge = Edge(node, self.depot)
            dnEdge.inverse_edge = ndEdge # sets the inverse edge
            ndEdge.inverse_edge = dnEdge
            # compute the Euclidean Distance as cost
            dnEdge.cost = math.sqrt((node.x - self.depot.x)**2 + (node.y - self.depot.y)**2)
            ndEdge.cost = dnEdge.cost # assume symetric costs
            # save in node a reference to the (depot, node) edge
            node.from_depot_edge = dnEdge
            node.to_depot_edge = ndEdge

    def are_routes_mergeable(self, node_a : Node, node_b : Node, route_a : Route, route_b : Route):
        is_different_route = route_a != route_b
        are_nodes_exterior = node_a.is_connected_to_depot and node_b.is_connected_to_depot
        is_total_demand_covered = self.vehicle_capacity >= route_a.demand + route_b.demand
        return is_different_route and are_nodes_exterior and is_total_demand_covered

    def get_depot_edge(self, route : Route, node : Node):
        origin = route.edges[0].origin
        end = route.edges[0].end
        return route.edges[0] if ( (origin == node and end == self.depot) or
            ( origin == self.depot and end == node)) else route.edges[-1]

    def are_multiple_edges(self, route: Route) -> bool:
        return len(route.edges) > 1
    
    def remove_depot_edge_from_route(self, route : Route, node : Node):
        depot_edge = self.get_depot_edge(route, node)
        route.remove_edge(depot_edge)
        # If there are multiple edges in a route, 
        # then origin will be interior, i.e., 
        # not directly connected to the depot
        if self.are_multiple_edges(route):
            node.is_connected_to_depot = False
        
    def merge(self, route_a : Route, node_a: Node, route_b : Route, node_b: Node, possible_common_edge : Edge):
        self.remove_depot_edge_from_route(route_a, node_a)
        self.remove_depot_edge_from_route(route_b, node_b)
        if route_a.edges[0].origin != self.depot :
            route_a.reverse()
        if route_b.edges[0].origin == self.depot :
            route_b.reverse()
        route_a.add_edge(possible_common_edge)
        route_a.demand += node_b.demand
        node_b.route = route_a
        for edge in route_b.edges:
            route_a.edges.append(edge)
            route_a.cost += edge.cost
            route_a.demand += edge.end.demand
            edge.end.route = route_a
        self.solution.cost -= possible_common_edge.savings
        self.solution.remove_route(route_b)

    def run(self) -> Solution:
        while (len(self.savings) > 0):
            possible_common_edge:Edge = self.savings.pop(0)
            origin:Node = possible_common_edge.origin
            end:Node = possible_common_edge.end
            route_a:Route = origin.route
            route_b:Route = end.route
            if ( self.are_routes_mergeable(origin, end, route_a, route_b) ):
                self.merge(route_a, origin, route_b, end, possible_common_edge)
        return self.solution

    