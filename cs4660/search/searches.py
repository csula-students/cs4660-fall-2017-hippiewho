"""
Searches module defines all different search algorithms
"""

try:
    import Queue as q
except ImportError:
    import queue as q

def bfs(graph, initial_node, dest_node):
    """
    Breadth First Search
    uses graph to do search from the initial_node to dest_node
    returns a list of actions going from the initial node to dest_node
    """
    visited = []
    queue =  q.Queue()
    edges = {}

    queue.put(initial_node)
    visited.append(initial_node)

    while not queue.empty():
        current_node = queue.get()

        for neighbor_node in graph.neighbors(current_node):

            if neighbor_node not in visited:
                queue.put(neighbor_node)
                visited.append(neighbor_node)

                current_cost = graph.distance(current_node, neighbor_node)

                if neighbor_node not in edges:
                    edges[neighbor_node] = (current_node, 1)
                elif neighbor_node in edges:
                    edges[neighbor_node] = (current_node, 1)

    final_paths = []
    to_node = dest_node
    from_node = edges[to_node][0]
    final_paths.append(to_node)

    # {  to_node  :  from_node , weight = 1)  }
    while from_node != initial_node:
        final_paths.append(from_node)

        to_node = from_node
        from_node = edges[to_node][0]
        if from_node == initial_node:
            final_paths.append(from_node)
            continue

    return final_paths.reverse()

def dfs(graph, initial_node, dest_node):
    """
    Depth First Search
    uses graph to do search from the initial_node to dest_node
    returns a list of actions going from the initial node to dest_node
    """
    visited = []
    queue =  q.LifoQueue()
    edges = {}

    queue.put(initial_node)
    visited.append(initial_node)

    while not queue.empty():
        current_node = queue.get()
        if current_node != dest_node:
        
           for neighbor_node in graph.neighbors(current_node):
                if neighbor_node not in visited:
                    queue.put(neighbor_node)
                    visited.append(neighbor_node)

                    if neighbor_node not in edges:
                        edges[neighbor_node] = (current_node)
                    elif neighbor_node in edges :
                        edges[neighbor_node] = (current_node)
        else:
            continue

    final_paths = []
    to_node = dest_node
    from_node = edges[to_node]
    final_paths.append(to_node)

    # { to_node : from_node }
    while from_node != initial_node:
        final_paths.append(from_node)

        to_node = from_node
        from_node = edges[to_node]
        if from_node == initial_node:
            final_paths.append(from_node)
            continue
        
    return final_paths.reverse()

def dijkstra_search(graph, initial_node, dest_node):
    """
    Dijkstra Search
    uses graph to do search from the initial_node to dest_node
    returns a list of actions going from the initial node to dest_node
    """
    visited = []
    queue =  q.PriorityQueue()
    edges = {}

    queue.put(initial_node)
    visited.append(initial_node)

    while not queue.empty():
        current_node = queue.get()
        cost = 0


        for neighbor_node in graph.neighbors(current_node):
            
            if current_node in edges:
                cost = edges[current_node][1]

            if neighbor_node not in visited:
                queue.put(neighbor_node)
                visited.append(neighbor_node)

                current_cost = graph.distance(current_node, neighbor_node)

                if neighbor_node not in edges:
                    edges[neighbor_node] = (current_node, current_cost + cost)
                elif neighbor_node in edges and (edges[neighbor_node][1] < (current_cost + cost)):
                    edges[neighbor_node] = (current_node, current_cost + edges[neighbor_node][1])

    final_paths = []
    to_node = dest_node
    from_node = edges[to_node][0]
    final_paths.append(to_node)

    # {  to_node  :  from_node , weight)  }
    while from_node != initial_node:
        final_paths.append(from_node)

        to_node = from_node
        from_node = edges[to_node][0]
        if from_node == initial_node:
            final_paths.append(from_node)
            continue

    return final_paths.reverse()

def a_star_search(graph, initial_node, dest_node):
    """
    A* Search
    uses graph to do search from the initial_node to dest_node
    returns a list of actions going from the initial node to dest_node
    """
    pass