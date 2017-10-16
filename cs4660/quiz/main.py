"""
quiz2!

Use path finding algorithm to find your way through dark dungeon!

Tecchnical detail wise, you will need to find path from node 7f3dc077574c013d98b2de8f735058b4
to f1f131f647621a4be7c71292e79613f9

TODO: implement BFS
TODO: implement Dijkstra utilizing the path with highest effect number
"""

import json
import codecs
try:
    import Queue as q
except ImportError:
    import queue as q

# http lib import for Python 2 and 3: alternative 4
try:
    from urllib.request import urlopen, Request
except ImportError:
    from urllib2 import urlopen, Request

GET_STATE_URL = "http://192.241.218.106:9000/getState"
STATE_TRANSITION_URL = "http://192.241.218.106:9000/state"

def get_state(room_id):
    """
    get the room by its id and its neighbor
    """
    body = {'id': room_id}
    return __json_request(GET_STATE_URL, body)

def transition_state(room_id, next_room_id):
    """
    transition from one room to another to see event detail from one room to
    the other.

    You will be able to get the weight of edge between two rooms using this method
    """
    body = {'id': room_id, 'action': next_room_id}
    return __json_request(STATE_TRANSITION_URL, body)

def __json_request(target_url, body):
    """
    private helper method to send JSON request and parse response JSON
    """
    req = Request(target_url)
    req.add_header('Content-Type', 'application/json; charset=utf-8')
    jsondata = json.dumps(body)
    jsondataasbytes = jsondata.encode('utf-8')   # needs to be bytes
    req.add_header('Content-Length', len(jsondataasbytes))
    reader = codecs.getreader("utf-8")
    response = json.load(urlopen(req, jsondataasbytes))
    return response

def bfs(start_id, end_id):
    visited = []
    edges = {}
    queue = q.Queue()
    parents = {}

    queue.put(start_id);
    visited.append(start_id)

    while not queue.empty():
        current_room_id = queue.get()
        current_room_state = get_state(current_room_id)

        for neighbor in current_room_state['neighbors']:
            neighbor_id = neighbor["id"]

            if neighbor_id not in visited:
                edge = transition_state(current_room_id, neighbor_id)
                edges[neighbor_id] = edge
                visited.append(neighbor_id)
                parents[neighbor_id] = current_room_id

                if neighbor_id != end_id:
                    queue.put(neighbor_id)
        
    final_path = []
    current = end_id
    final_path.append(current)

    while current in parents:
        final_path.append(parents[current])
        current = parents[current]


    final_path.reverse()
    print_path(final_path, end_id)


def dijkstra(start_id, end_id):
    # List of visited nodes
    visited = []
    # Edges of neigbors - { node_to : {node_from , current_weight) }
    edges = {}
    queue = q.PriorityQueue()
    
    queue.put(start_id)

    while not queue.empty():
        current_room_state = get_state(queue.get())
        current_room_id = current_room_state["id"]
        current_cost = 0

        if current_room_id in edges:
            current_cost = edges[current_room_id][2]

        for neighbor in current_room_state["neighbors"]:
            neighbor_id = neighbor["id"]
            if neighbor_id not in visited:
                edge_state = transition_state(current_room_id, neighbor_id)
                effect_transition = edge_state["event"]["effect"]

                queue.put(neighbor_id)
                visited.append(neighbor_id)
                
                if neighbor_id not in edges:
                    edges[neighbor_id] = (current_room_id, neighbor_id, (effect_transition + current_cost))
                elif neighbor_id in edges and (effect_transition + current_cost) > edges[neighbor_id][1]:
                    edges[neighbor_id] = (current_room_id, neighbor_id, (effect_transition + current_cost))

    current = end_id
    final_paths = []    
    final_paths.append(current)

    while (current != start_id) and edges[current] :
        current = edges[current][0]
        final_paths.append(current)

    final_paths.reverse()

    print_path(final_paths, end_id)


def print_path(path, end_id):
    damage = 0

    for i in range(0 , len(path) - 1):
        from_id = path[i]
        to_id   = path[i + 1]

        current_room = get_state(from_id)
        current_transition_state = transition_state(from_id, to_id)
        
        name_of_current_room = current_room["location"]["name"]
        name_of_next_room = current_transition_state['action']
        effect = current_transition_state['event']['effect']
        description = current_transition_state['event']['description']

        damage += effect
        if effect <= 0 :
            print("Moved From %s (ID: %s) to %s (ID: %s). %s and caused %i damage." % (name_of_current_room, from_id, name_of_next_room, to_id, description, effect))
        elif effect > 0 :
            print("Moved From %s (ID: %s) to %s (ID: %s). %s You've recovered %i HP." % (name_of_current_room, from_id, name_of_next_room, to_id, description, effect))
            
    print("\nTotal Damage Taken: %i \n" % damage)

if __name__ == "__main__":
    # Your code starts here
    # empty_room = get_state('7f3dc077574c013d98b2de8f735058b4')
    # print(empty_room)
    # print(transition_state(empty_room['id'], empty_room['neighbors'][0]['id']))
    start_id = '7f3dc077574c013d98b2de8f735058b4'
    end_id = 'f1f131f647621a4be7c71292e79613f9'
    
    # Searches:
    bfs(start_id, end_id)
    dijkstra(start_id, end_id)
