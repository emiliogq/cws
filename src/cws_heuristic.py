from vrp_objects import Node, Edge, Route, Solution
import math
import operator

vehCap = 100.0 # update vehicle capacity for each instance
instanceName = 'A-n80-k10' # name of the instance
# txt file with the VRP instance data (nodeID, x, y, demand)
filename = 'data/' + instanceName + '_input_nodes.txt'

def read_nodes(filename: str):
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

depot, destinations = read_nodes(filename)

for node in destinations:
    dnEdge = Edge(depot, node) # creates (depot, node) edge
    ndEdge = Edge(node, depot)
    dnEdge.inverse_edge = ndEdge # sets the inverse edge
    ndEdge.inverse_edge = dnEdge
    # compute the Euclidean Distance as cost
    dnEdge.cost = math.sqrt((node.x - depot.x)**2 + (node.y - depot.y)**2)
    ndEdge.cost = dnEdge.cost # assume symetric costs
    # save in node a reference to the (depot, node) edge
    node.from_depot_edge = dnEdge
    node.to_depot_edge = ndEdge

savingsList = []
for i in range(len(destinations)):
    destination_a = destinations[i]
    for j in range(i+1, len(destinations)):
        destination_b = destinations[j]
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
        savingsList.append(ijEdge)



savingsList.sort(key = operator.attrgetter("savings"), reverse = True)
# TODO creo que el ej 2 iria aqui haciendo orden random con una exponencial o triangular

sol = Solution(destinations)

def are_routes_mergeable(node_a : Node, node_b : Node, route_a : Route, route_b : Route):
    is_different_route = route_a != route_b
    are_nodes_exterior = node_a.is_connected_to_depot and node_b.is_connected_to_depot
    is_total_demand_covered = vehCap >= route_a.demand + route_b.demand
    return is_different_route and are_nodes_exterior and is_total_demand_covered

def get_depot_edge(route : Route, node : Node):
    origin = route.edges[0].origin
    end = route.edges[0].end
    return route.edges[0] if ( (origin == node and end == depot) or
        ( origin == depot and end == node)) else route.edges[-1]

def iterative():
    while (len(savingsList) > 0):
        possible_common_edge:Edge = savingsList.pop(0)
        origin:Node = possible_common_edge.origin
        end:Node = possible_common_edge.end
        route_a:Route = origin.route
        route_b:Route = end.route
        if ( are_routes_mergeable(origin, end, route_a, route_b) ):
            merge(route_a, origin, route_b, end, possible_common_edge)

def remove_depot_edge_from_route(route : Route, node : Node):
    depot_edge = get_depot_edge(route, node)
    route.remove_edge(depot_edge)
    # If there are multiple edges in a route, 
    # then origin will be interior, i.e., 
    # not directly connected to the depot
    if len(route.edges) > 1:
        node.is_connected_to_depot = False
    
def merge(route_a : Route, node_a: Node, route_b : Route, node_b: Node, possible_common_edge : Edge):
    remove_depot_edge_from_route(route_a, node_a)
    remove_depot_edge_from_route(route_b, node_b)
    if route_a.edges[0].origin != depot :
        route_a.reverse()
    if route_b.edges[0].origin == depot :
        route_b.reverse()
    route_a.add_edge(possible_common_edge)
    route_a.demand += node_b.demand
    node_b.route = route_a
    for edge in route_b.edges:
        route_a.edges.append(edge)
        route_a.cost += edge.cost
        route_a.demand += edge.end.demand
        edge.end.route = route_a
    sol.cost -= possible_common_edge.savings
    sol.remove_route(route_b)

iterative()
print(sol)