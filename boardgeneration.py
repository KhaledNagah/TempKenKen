import numpy as np
from board import board
from coordinate import Coordinate
from constraint import Arithmetic_Constraint


"""
Creates a randomly generated board where there are no duplicates
in each row/column
"""
def random_board(size):
   
    vals = list(range(1, size + 1))

    board = np.zeros((size, size), dtype=int)
    for row in range(size):
        while True:
            board[row, :] = 0
            for col in range(size):
                possible = set(vals) - set(list(board[row, :]) + list(board[:, col]))

                if len(possible) == 0:
                    break
                board[row, col] = np.random.choice(list(possible))
            else:
                break
    return board
'''
stub classes used just for partitioning
'''
class Graph(object):
    def __init__(self, size: int):
        # Start with one node for every coordinate location on the board
        self._nodes = [Node(i) for i in range(size*size)]

        # Set up the edges for each node
        self._edges = []
        for n in range(size*size):
            x = n // size
            y = n % size

            edges = [(x, y + 1), (x, y - 1), (x + 1, y), (x - 1, y)]

            to_add = []
            for e in edges:
                if e[0] >= 0 and e[0] < size and e[1] >= 0 and e[1] < size:
                    to_add.append(self._nodes[e[0] * size + e[1]])
            self._edges.append(to_add)
        pass

    def merge(self, one, two):

        # Get the unique set of edges that border the merged node
        new_edges = list(set(self._edges[one] + self._edges[two]))

        # Merge them together
        self._nodes[one].add(self._nodes[two])

        # Each node would have had the other one as an edge, so remove these
        new_edges.remove(self._nodes[one])
        new_edges.remove(self._nodes[two])

        # Update the edges on the merged node
        self._edges[one] = new_edges

        # Now we have to update the other node connections so they point to one
        # instead of two
        for edge in self._edges:
            if self._nodes[two] in edge:
                edge.remove(self._nodes[two])

                # There is a possibility where the first node was already inside edges,
                # in this case we do not need to do anything
                if self._nodes[one] not in edge:
                    edge.append(self._nodes[one])

        # Remove the second node from the structure
        del self._nodes[two]
        del self._edges[two]

    @property
    def nodes(self):
        return self._nodes

    @property
    def edges(self):
        return self._edges


class Node(object):
    def __init__(self, start):
        self._coords = [start]

    def __repr__(self):
        return 'Coords: ' + str(self.coords)

    @property
    def coords(self):
        return self._coords

    def add(self, node):
        self._coords += node.coords

    def __eq__(self, other):
        return self.coords == other.coords

    def __hash__(self):
        return hash(str(self.coords))
'''
end of stub classes
'''


'''
Partitions a board size into a set of groups to add the arithmetic constraints
'''
def partition_board(size, max_partition_size,
                    initial_choice_size_factor=2,
                    merge_size_factor=0.8,
                    average_size_stop=3):

    graph = Graph(size)

    average_node_size = 1
    i=1;
    # Repeatedly merge nodes of the graph until some conditions are satisfied
    while average_node_size < average_size_stop:
        # Calculate probability of picking a node as a starting merge point
        p = np.ones(len(graph.nodes))

        for i, n in enumerate(graph.nodes):
            p[i] /= np.exp(len(n.coords))**initial_choice_size_factor
        p /= np.sum(p)
        node_idx = np.random.choice(list(range(len(graph.nodes))), p=p)

        # Create some probabilities of picking which node to merge with
        p = np.ones(len(graph.edges[node_idx]))
        for i, n in enumerate(graph.edges[node_idx]):
            p[i] /= np.exp(len(n.coords))**merge_size_factor
        p /= np.sum(p)

        merge_node = np.random.choice(graph.edges[node_idx], p=p)
        merge_idx = graph.nodes.index(merge_node)

        if len(graph.nodes[node_idx].coords) + len(merge_node.coords) > max_partition_size:
            continue

        graph.merge(node_idx, merge_idx)

        node_lengths = [len(n.coords) for n in graph.nodes]

        average_node_size = np.average(node_lengths)
    partitions = [n.coords for n in graph.nodes]

    return partitions
  
'''
the partitioning function returns the coordinates as index so we have to change it to x and y
'''
def idxtocoord(partitions,size):
    x=0
    z=0
    partitioncoord = [[int(n//size),n%size] for i in partitions for n in i]
    for i in partitions:
        for n in range(len(i)):
            partitions[x][n]=partitioncoord[z]
            z=z+1
        x=x+1
    return partitions
  
  
'''
calculating the possible sum constraints to every partition
'''

def generatingsum(board,partitions):
    sum=0
    values=[]
    for i in partitions:
        for j in i:
            sum=sum+board[j[0]][j[1]]
        values.append(sum)
        sum=0
    return values
  
'''
adding the arithmetic constraint to the given board
'''
  
def addArithmeticConstraints(board,partitions,values):
    constraintslist=[]
    x=0
    z=0
    for i in partitions:
        for n in range(len(i)):
            partitions[x][n]=board.get_coordinate(partitions[x][n][0],partitions[x][n][1])
            z=z+1
        x=x+1
    for i in range(len(values)):
        constraintslist.append(Arithmetic_Constraint(partitions[i],values[i]))
    for i in constraintslist:
        board.add_constraint(i)
    x=0
    z=0
    for i in partitions:
        for n in range(len(i)):
            coord=partitions[x][n]
            coord.add_constraint(constraintslist[x])
        x=x+1
  
'''
function that will sum up every step and return an object of board to be used in solving

'''

def createBoard(size):
  board1=random_board(size)
  print(board1)
  partitions=partition_board(size,size)
  partitions=idxtocoord(partitions,size)
  print(partitions)
  values=generatingsum(board1,partitions)
  BOARD = board(size)
  #BOARD.initialize_RCconstraint()
  addArithmeticConstraints(BOARD,partitions,values)
  return BOARD
