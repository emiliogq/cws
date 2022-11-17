from vrp_objects import Node, Edge, Route, Solution
import math
import operator

vehCap = 100.0 # update vehicle capacity for each instance
instanceName = 'A-n80-k10' # name of the instance
# txt file with the VRP instance data (nodeID, x, y, demand)
fileName = 'data/' + instanceName + '_input_nodes.txt'

with open(fileName) as instance:
    i = 0
    nodes = []
    for line in instance:
        # array data with node data: x, y demand
        data = [float(x) for x in line.split()]
        aNode = Node(i, data[0], data[1], data[2])
        nodes.append(aNode)
        i += 1

depot = nodes[0] # node 0 is depot
for node in nodes[1:]: # exclude depot
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
for i in range(1, len(nodes) - 1): # excludes depot
    iNode = nodes[i]
    for j in range(i + 1, len(nodes)):
        jNode = nodes[j]
        ijEdge = Edge(iNode, jNode) # creates the (i, j) edge
        jiEdge = Edge(jNode, iNode)
        ijEdge.inverse_edge = jiEdge # sets the inverse edge
        jiEdge.inverse_edge = ijEdge
        # compute the Euclidean distance as cost
        ijEdge.cost = math.sqrt((jNode.x - iNode.x)**2 + (jNode.y - iNode.y)**2)
        jiEdge.cost = ijEdge.cost # assume symmectir costs
        # compute savins as proposed by Clark & Wright
        ijEdge.savings = iNode.to_depot_edge.cost + jNode.from_depot_edge.cost - ijEdge.cost
        jiEdge.savings = ijEdge.savings
        # save one edge in the savings list
        savingsList.append(ijEdge)



savingsList.sort(key = operator.attrgetter("savings"), reverse = True)
# TODO creo que el ej 2 iria aqui haciendo orden random con una exponencial o triangular

sol = Solution()
#### ...
