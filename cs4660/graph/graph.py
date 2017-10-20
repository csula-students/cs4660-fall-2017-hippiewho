"""
graph module defines the knowledge representations files

A Graph has following methods:

* adjacent(node_1, node_2)
    - returns true if node_1 and node_2 are directly connected or false otherwise
* neighbors(node)
    - returns all nodes that is adjacency from node
* add_node(node)
    - adds a new node to its internal data structure.
    - returns true if the node is added and false if the node already exists
* remove_node
    - remove a node from its internal data structure
    - returns true if the node is removed and false if the node does not exist
* add_edge
    - adds a new edge to its internal data structure
    - returns true if the edge is added and false if the edge already existed
* remove_edge
    - remove an edge from its internal data structure
    - returns true if the edge is removed and false if the edge does not exist
"""

from io import open
from operator import itemgetter

def construct_graph_from_file(graph, file_path):
    """
    TODO: read content from file_path, then add nodes and edges to graph object

    note that grpah object will be either of AdjacencyList, AdjacencyMatrix or ObjectOriented

    In example, you will need to do something similar to following:

    1. add number of nodes to graph first (first line)
    2. for each following line (from second line to last line), add them as edge to graph
    3. return the graph
    """
    file = open(file_path)
    text = file.read()
    lines = text.split("\n")
    number_of_nodes = int(lines[0])
    lines = lines[1:]

    for i in range(0, number_of_nodes):
        graph.add_node(Node(i))

    for line in lines:
        if line != "":
            line = line.split(":")
            graph.add_edge(Edge(Node(int(line[0])), Node(int(line[1])), int(line[2])))
    return graph

class Node(object):
    """Node represents basic unit of graph"""
    def __init__(self, data):
        self.data = data

    def __str__(self):
        return 'Node({})'.format(self.data)
    def __repr__(self):
        return 'Node({})'.format(self.data)

    def __eq__(self, other_node):
        return self.data == other_node.data
    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(self.data)

class Edge(object):
    """Edge represents basic unit of graph connecting between two edges"""
    def __init__(self, from_node, to_node, weight):
        self.from_node = from_node
        self.to_node = to_node
        self.weight = weight
    def __str__(self):
        return 'Edge(from {}, to {}, weight {})'.format(self.from_node, self.to_node, self.weight)
    def __repr__(self):
        return 'Edge(from {}, to {}, weight {})'.format(self.from_node, self.to_node, self.weight)

    def __eq__(self, other_node):
        return self.from_node == other_node.from_node and self.to_node == other_node.to_node and self.weight == other_node.weight
    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash((self.from_node, self.to_node, self.weight))

class AdjacencyList(object):
    """
    AdjacencyList is one of the graph representation which uses adjacency list to
    store nodes and edges
    """
    def __init__(self):
        # adjacencyList should be a dictonary of node to edges
        self.adjacency_list = {}

    def adjacent(self, node_1, node_2):
        for node in self.adjacency_list[node_1]:
            if node.to_node == node_2:
                return True
        return False

    def neighbors(self, node):
        l = []
        for e in self.adjacency_list[node]:
            l.append(e.to_node)     
        return l

    def add_node(self, node):
        if node not in self.adjacency_list:
            self.adjacency_list[node] = []
            return True
        else:
            return False

    def remove_node(self, node):
        if node in self.adjacency_list:
            for n, edges in self.adjacency_list.items():
               self.adjacency_list[n] = []
            del self.adjacency_list[node]
            return True
        else:
            return False

    def add_edge(self, edge):
        if edge.from_node in self.adjacency_list and edge not in self.adjacency_list[edge.from_node]:
            self.adjacency_list[edge.from_node].append(edge)
            return True
        else:
            return False

    def remove_edge(self, edge):
        if self.adjacency_list[edge.from_node] != [] and edge in self.adjacency_list[edge.from_node]:
            self.adjacency_list[edge.from_node].remove(edge)
            return True
        else:
            return False

    def distance(self, node_1, node_2):
        for current in self.adjacency_list[node_1]:
            if current.to_node == node_2:
                return current.weight

class AdjacencyMatrix(object):
    def __init__(self):
        # adjacency_matrix should be a two dimensions array of numbers that
        # represents how one node connects to another
        self.adjacency_matrix = []
        # in additional to the matrix, you will also need to store a list of Nodes
        # as separate list of nodes
        self.nodes = []

    def adjacent(self, node_1, node_2):
        if self.adjacency_matrix[node_1.data][node_2.data] == None or node_1 not in self.nodes or node_2 not in self.nodes:
            return False
        else:
            return True
            
    def neighbors(self, node):
        l = []
        position = 0
        if node not in self.nodes:
            return False   
        else:
            for n in self.adjacency_matrix[node.data]:
                if n != None:
                    l.append(Node(position))
                position += 1
        return l

    def add_node(self, node):
        if node not in self.nodes:
            self.nodes.append(node)
            for i in self.adjacency_matrix:
                i.append(None)
            self.adjacency_matrix.append([None] * len(self.nodes))
            return True
        else:
            return False
        

    def remove_node(self, node):
        if node in self.nodes:
            for n in self.adjacency_matrix:
                del n[self.__get_node_index(node)]
            self.nodes.remove(node)

            return True
        else:
            return False

    def add_edge(self, edge):
        if self.adjacency_matrix[self.__get_node_index(edge.from_node)][self.__get_node_index(edge.to_node)] is None:
            self.adjacency_matrix[self.__get_node_index(edge.from_node)][self.__get_node_index(edge.to_node)] = edge.weight
            return True
        else:
            return False

    def remove_edge(self, edge):
        tonode = edge.to_node
        fromnode = edge.from_node

        if self.adjacency_matrix[self.__get_node_index(fromnode)][self.__get_node_index(tonode)] is None:
            return False
        else:
            self.adjacency_matrix[self.__get_node_index(fromnode)][self.__get_node_index(tonode)] = None

            return True

    def __get_node_index(self, node):
        """helper method to find node index"""
        return self.nodes.index(node)

    def distance(self, node_1, node_2):
        if self.adjacency_matrix[self.__get_node_index(node_1)][self.__get_node_index(node_2)]:
            return self.adjacency_matrix[self.__get_node_index(node_1)][self.__get_node_index(node_2)]
            
class ObjectOriented(object):
    """ObjectOriented defines the edges and nodes as both list"""
    def __init__(self):
        # implement your own list of edges and nodes
        self.edges = []
        self.nodes = []

    def adjacent(self, node_1, node_2):
        if node_1 in self.nodes and node_2 in self.nodes:
            for e in self.edges:
                if e.from_node == node_1 and e.to_node == node_2:
                    return True
        return False
            
    def neighbors(self, node):
        l = []
        if node in self.nodes:
            for e in self.edges:
                if e.from_node == node:
                    l.append(e.to_node)
        return l

    def add_node(self, node):
        if node not in self.nodes:
            self.nodes.append(node)
            return True
        else:
            return False

    def remove_node(self, node):
        if node in self.nodes:
            self.nodes.remove(node)
            for e in self.edges:
                if node == e.from_node or node == e.to_node:
                    self.edges.remove(e)
            return True
        else:
            return False  

    def add_edge(self, edge):
        if edge not in self.edges:
            self.edges.append(edge)
            return True
        else:
            return False

    def remove_edge(self, edge):
        if edge in self.edges:
            self.edges.remove(edge)
            return True
        else:
            return False

    def distance(self, node_1, node_2):
        for i in self.edges:
            if i.to_node == node_2 and i.from_node == node_1:
                return i.weight