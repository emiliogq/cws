
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