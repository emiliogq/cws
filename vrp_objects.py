class Node:
    def __init__(self, ID, x, y, demand):
        self.Id = ID # node identifier (depot ID = 0)
        self.x = x # Euclidean x-coordinate
        self.y = y # Euclidean y-coordinate
        self.demand = demand # demand (is 0 for depot and positive for others)
        self.route = None # route to which node belongs
        self.is_connected_to_depot = False # an interior node is not connected to depot
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
    
    def reverse(self): # e.g. 0 -> 2 -> 6 -> 0 becomes 0 -> 6 -> 2 -> 0
        size = len(self.edges)
        for i in range(size):
            edge = self.edges[i]
            invEdge = edge.invEdge
            self.edges.remove(edge)
            self.edges.insert(0, invEdge)

class Solution:
    last_ID = -1 #counts the number of solutions, starts with 0
    def __init__(self):
        Solution.last_ID += 1
        self.ID = Solution.last_ID
        self.routes = [] # routes in this solution
        self.cost = 0.0 # cost of this solution
        self.demand = 0.0 # total demand covered by this solution