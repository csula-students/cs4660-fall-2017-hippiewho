"""
utils package is for some quick utility methods

such as parsing
"""
import graph


class Tile(object):
    """Node represents basic unit of graph"""
    def __init__(self, x, y, symbol):
        self.x = x
        self.y = y
        self.symbol = symbol

    def __str__(self):
        return 'Tile(x: {}, y: {}, symbol: {})'.format(self.x, self.y, self.symbol)
    def __repr__(self):
        return 'Tile(x: {}, y: {}, symbol: {})'.format(self.x, self.y, self.symbol)

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.x == other.x and self.y == other.y and self.symbol == other.symbol
        return False
    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(self.x + self.y + self.symbol)



def parse_grid_file(graph, file_path):
    """
    ParseGridFile parses the grid file implementation from the file path line
    by line and construct the nodes & edges to be added to graph

    Returns graph object
    """
    # TODO: read the filepaht line by line to construct nodes & edges

    # TODO: for each node/edge above, add it to graph
    file = open(file_path)
    lines = file.read().split('\n')[1:-2]
    
    count = 0
    grid = []

    count = 0

    for i in lines:
        row = []
        for j in range(1, len(i) - 2 , 2):
            row.append(i[j:j + 2])
        lines[count] = row
        count += 1

    grid = lines

    for s in grid:
        print s

    tiles = {}

    for Y in range(len(grid)):
        for x in range (len(grid[0])):
            tile = Tile(x, y, grid[y][x])
            tiles[(x, y)] = tile           
            graph.add_node(Node(tile))

    for Y in range(len(grid)):
        for x in range (len(grid[0])):
            current_tile = Tile(x, y, grid[y][x])

            if current_tile.symbol == "##":
                continue

            if (x, y - 1) in tiles:
                upper_tile = tiles[(x, y - 1)]
                if upper_tile.symbol != "##":
                    print Edge(Node(current_tile), Node(upper_tile), 1)
                    graph.add_edge(Edge(Node(current_tile), Node(upper_tile), 1))   

            if (x + 1, y) in tiles:
                right_tile = tiles[(x + 1, y)]
                if right_tile.symbol != "##":
                    graph.add_edge(Edge(Node(current_tile), Node(right_tile), 1))

            if (x - 1, y) in tiles:
                left_tile = tiles[(x - 1, y)]
                if left_tile.symbol != "##":
                    graph.add_edge(Edge(Node(current_tile), Node(left_tile), 1))

            if (x, y + 1) in tiles:
                lower_tile = tiles[(x, y + 1)]
                if lower_tile.symbol != "##":
                    graph.add_edge(Edge(Node(current_tile), Node(lower_tile), 1))

    return graph

def convert_edge_to_grid_actions(edges):
    """
    Convert a list of edges to a string of actions in the grid base tile

    e.g. Edge(Node(Tile(1, 2), Tile(2, 2), 1)) => "S"
    """
    return ""

# grid_4_path = '../test/fixtures/grid-4.txt'
# graph_4 = parse_grid_file(graph.AdjacencyList(), grid_4_path)
