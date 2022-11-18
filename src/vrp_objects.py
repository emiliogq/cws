class Node:
    def __init__(self, ID, x, y, demand):
        self.ID = ID # node identifier (depot ID = 0)
        self.x = x # Euclidean x-coordinate
        self.y = y # Euclidean y-coordinate
        self.demand = demand # demand (is 0 for depot and positive for others)
        self.route = None # route to which node belongs
        self.is_connected_to_depot = True # an interior node is not connected to depot
        self.from_depot_edge = None # edge (arc) from depot to this node
        self.to_depot_edge = None # edge (arc) from this node to depot

class Edge:
    def __init__(self, origin, end):
        self.origin = origin # origin node of the edge (arc)
        self.end = end # end node of the edge (arc)
        self.cost = 0.0 # edge cost
        self.savings = 0.0 # edge savings (Clarke & Wright)
        self.inverse_edge = None # inverse edge (arc)
    
    
class Route:
    def __init__(self):
        self.cost = 0.0 # cost of this route
        self.edges = [] # sorted edges in this route
        self.demand = 0.0 # total demand covered by this route

    def add_node(self, node : Node):
        self.demand += node.demand
        node.route = self
        node.is_connected_to_depot = True
        self.add_edge(node.from_depot_edge)
        self.add_edge(node.to_depot_edge)
    
    def add_edge(self, edge: Edge):
        self.cost += edge.cost
        self.edges.append(edge)

    def remove_edge(self, edge: Edge):
        self.cost -= edge.cost
        self.edges.remove(edge)

    def reverse(self): # e.g. 0 -> 2 -> 6 -> 0 becomes 0 -> 6 -> 2 -> 0
        size = len(self.edges)
        for i in range(size):
            edge = self.edges[i]
            invEdge = edge.inverse_edge
            self.edges.remove(edge)
            self.edges.insert(0, invEdge)
    def __str__(self):
        s = str(0)
        for edge in self.edges:
            s += "-" + str(edge.end.ID)
        return "Route: " + s + " || cost = " + "{:.{}f}".format(self.cost, 2) + "\n"

class Solution:
    last_ID = -1 #counts the number of solutions, starts with 0
    def __init__(self, destinations : list[Node]):
        Solution.last_ID += 1
        self.ID = Solution.last_ID
        self.routes = [] # routes in this solution
        self.cost = 0.0 # cost of this solution
        self.demand = 0.0 # total demand covered by this solution
        self.create_routes(destinations)
    
    def create_routes(self, destinations):
        for node in destinations:
            route = Route()
            route.add_node(node)
            self.add_route(route)

    def add_route(self, route : Route):
        self.routes.append(route)
        self.cost += route.cost
        self.demand += route.demand
   
    def remove_route(self, route: Route):
        self.routes.remove(route)
    
    def __str__(self):
        s = "Cost of C&W savings sol = "+ "{:.{}f}".format(self.cost,2)+"\n"
        for route in self.routes:
            s += str(route)
        return s