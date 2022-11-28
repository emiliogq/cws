from vrp.routes.route import Route


class Solution:
    last_ID = -1 #counts the number of solutions, starts with 0
    def __init__(self, destinations : list):
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