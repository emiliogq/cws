from vrp.nodes.node import Node
from vrp.edges.edge import Edge

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