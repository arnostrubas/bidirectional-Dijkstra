import networkx as nx # type: ignore
from functools import partial
from js import window # type: ignore
import json
import heapq

#region custom_classes
class Node:
    def __init__(self, id, d_f = None, pi_f = None, state_f = None, d_b = None, pi_b = None, state_b = None):
        self.id = id
        self.d_f = d_f
        self.pi_f = pi_f
        self.state_f = state_f
        self.d_b = d_b
        self.pi_b = pi_b
        self.state_b = state_b

    def __lt__(self, other):
        if self is None or other is None:
            return NotImplemented
        return self.id < other.id
    
    def __str__(self):
        return str(self.id)


class Queue(list):
    def __init__(self, forward = True):
        self.count = 0
        self.forward = forward

    def insert(self, element):
        if (self.forward):
            heapq.heappush(self, (element.d_f, element))
        else:
            heapq.heappush(self, (element.d_b, element))
        self.count += 1

    def update(self, element):
        if (self.forward):
            heapq.heappush(self, (element.d_f, element))
        else:
            heapq.heappush(self, (element.d_b, element))

    def extractMin(self):
        d, element = heapq.heappop(self)
        if (self.forward):
            while element.d_f != d:
                if len(self) == 0:
                    return None
                d, element = heapq.heappop(self)
        else:
            while element.d_b != d:
                if len(self) == 0:
                    return None
                d, element = heapq.heappop(self)
        self.count -= 1
        return element
    
    def isEmpty(self):
        return self.count == 0

#endregion

#region json_functions

def graph_to_json(G):
    nodes = []
    for node in G.nodes:
        label = str(node.id)
        if(node.id == -1):
            label = "S"
        elif (node.id == 0):
            label ="T"
        nodes.append({
            "data": { 
                "label": label,
                "id": str(node.id),
                "d_f": node.d_f,
                "pi_f": node.pi_f.id if node.pi_f else None,
                "state_f": node.state_f,
                "d_b": node.d_b,
                "pi_b": node.pi_b.id if node.pi_b else None,
                "state_b": node.state_b
            }
        })

    edges = []
    for u, v, data in G.edges(data=True):
        edges.append({
            "data": {
                "id": data['id'],
                "source": str(u.id), 
                "target": str(v.id),  
                "weight": data['weight'],
                "state": data['state']
            }
        })

    json_data = {
        "elements": {
            "nodes": json.dumps(nodes),
            "edges": json.dumps(edges)
        }
    }
    return json.dumps(json_data)

def queue_to_json(queue, forward):
    nodes = []
    for d, node in queue:
        if(forward and node.d_f == d): nodes.append((d, node.id))
        if(not forward and node.d_b == d): nodes.append((d, node.id))
    return json.dumps({
        "queue": nodes
    })

#endregion

#region algorithms and their functions
def node_on_path(node):
    node.state_f = "PATH"
    node.state_b = "PATH"

def edge_on_path(G, id1, id2):
    G[node_from_graph(G, id1)][node_from_graph(G, id2)]['state'] = "PATH"

def NCPP(G, end):
    "Dijkstra"
    if end == 0: 
        t = node_from_graph(G, 0)
        node_on_path(t)
        prev = t
        node = t.pi_f
        while node is not None:
            node_on_path(node)
            edge_on_path(G, node.id, prev.id)
            prev = node
            node = node.pi_f
            
    'same vertex closed'
    if end == 1:
        minimum = None
        middle_node = None
        for node in G.nodes:
            if (not minimum or node.d_f + node.d_b < minimum):
                minimum = node.d_f + node.d_b
                middle_node = node
        pred = middle_node
        while pred is not None:
            node_on_path(pred)
            if (pred.pi_f): edge_on_path(G, pred.pi_f.id, pred.id)
            pred = pred.pi_f

        pred = middle_node
        while pred is not None:
            node_on_path(pred)
            if (pred.pi_b): edge_on_path(G, pred.id, pred.pi_b.id)
            pred = pred.pi_b
        

        

def w(graph, u, v):
    return graph[u][v]['weight']

def init(G, s, t=None):
    for node in G.nodes:
        node.d_f = 999999999
        node.pi_f = None
        node.state_f = "UNVISITED"
        node.d_b = 999999999
        node.pi_b = None
        node.state_b = "UNVISITED"
    s.d_f = 0
    s.state_f = "OPEN"
    if (t):
        t.d_b = 0
        t.state_b = "OPEN"

def Dijkstra(G, w, s, t):
    init(G, s)
    Q = Queue()
    Q.insert(s)
    yield Q
    while not Q.isEmpty():
        v = Q.extractMin()
        v.state_f = "CLOSED"
        yield Q                     # for visualisation purposes
        if (v == t):
            NCPP(G, 0)
            yield Q
            return
        for u in sorted(G.successors(v), key=lambda node: node.id):
            if u.state_f == "UNVISITED":
                u.d_f = v.d_f + w(v, u)
                u.state_f = "OPEN"
                u.pi_f = v
                Q.insert(u)
                yield Q             # for visualisation purposes
            elif u.state_f == "OPEN":
                if v.d_f + w(v, u) < u.d_f:
                    u.d_f = v.d_f + w(v, u)
                    u.pi_f = v
                    Q.update(u) 
                    yield Q         # for visualisation purposes
    return None
#endregion

def bidirectional_Dijkstra_1(G, w, s, t):
    """
    Search = after one vertex \n
    End = same vertex close
    """
    init(G, s, t)
    Q_f = Queue()
    Q_f.insert(s)
    Q_b = Queue(False)
    Q_b.insert(t)
    fwd = True
    yield Q_f, Q_b                          # for visualisation purposes
    while (not Q_f.isEmpty()) and (not Q_b.isEmpty()):
        if (fwd):
            v = Q_f.extractMin()
            v.state_f = "CLOSED"
            yield Q_f, Q_b                  # for visualisation purposes
            if (v.state_b == "CLOSED"):
                NCPP(G, 1)
                yield Q_f, Q_b
                return None                 
            for u in sorted(G.successors(v), key=lambda node: node.id):
                if u.state_f == "UNVISITED":
                    u.d_f = v.d_f + w(v, u)
                    u.state_f = "OPEN"
                    u.pi_f = v
                    Q_f.insert(u)
                    yield Q_f, Q_b            # for visualisation purposes
                elif u.state_f == "OPEN":
                    if v.d_f + w(v, u) < u.d_f:
                        u.d_f = v.d_f + w(v, u)
                        u.pi_f = v
                        Q_f.update(u) 
                        yield Q_f, Q_b       # for visualisation purposes
            fwd = not fwd
        else:
            v = Q_b.extractMin()
            v.state_b = "CLOSED"
            yield Q_f, Q_b                    # for visualisation purposes
            if (v.state_f == "CLOSED"):
                NCPP(G, 1)
                yield Q_f, Q_b
                return None  
            for u in sorted(G.predecessors(v), key=lambda node: node.id):
                if u.state_b == "UNVISITED":
                    u.d_b = v.d_b + w(u, v)
                    u.state_b = "OPEN"
                    u.pi_b = v
                    Q_b.insert(u)
                    yield Q_f, Q_b            # for visualisation purposes
                elif u.state_b == "OPEN":
                    if v.d_b + w(u, v) < u.d_b:
                        u.d_b = v.d_b + w(u, v)
                        u.pi_b = v
                        Q_b.update(u) 
                        yield Q_f, Q_b       # for visualisation purposes
            fwd = not fwd
    return None



#region visualisation functions
def node_from_graph(G, id):
    for node in G.nodes:
        if node.id == id:
            return node
    return None

def visualise_Dijkstra(G):
    s = node_from_graph(G, -1) 
    t = node_from_graph(G, 0)
    runner = Dijkstra(G, partial(w, G), s, t)
    result = []
    for queue in runner:
        data = {
            "graph": graph_to_json(G),
            "queue_f": queue_to_json(queue, True),
            "queue_b": None
        } 
        result.append(json.dumps(data))
    res =  {
        "data": result
    }
    return json.dumps(res)

def visualise_biDijkstra(G, search, end):
    s = node_from_graph(G, -1) 
    t = node_from_graph(G, 0)
    runner = bidirectional_Dijkstra_1(G, partial(w, G), s, t)
    result = []
    for queue_f, queue_b in runner:
        data = {
            "graph": graph_to_json(G),
            "queue_f": queue_to_json(queue_f, True),
            "queue_b": queue_to_json(queue_b, False),
        } 
        result.append(json.dumps(data))
    res =  {
        "data": result,
    }
    return json.dumps(res)

def run_algorithm(graph_dict):
    search = graph_dict["search"]
    end = graph_dict["end"]
    graph_dict = graph_dict["graph"]
    nodes = graph_dict["nodes"]
    edges = graph_dict["edges"]

    G = nx.DiGraph()
    for node in nodes:
        n = Node(int(node["id"]))
        G.add_node(n)
    for edge in edges:
        u_id = edge["source"]
        v_id = edge["target"]
        u = node_from_graph(G, int(u_id))
        v = node_from_graph(G, int(v_id))
        weight = edge["weight"]
        G.add_edges_from([(u, v, {'weight': int(weight), 'state': 'EMPTY', 'id': edge["id"]})])
    

    #decide which algorithm to run
    if (search == "Dijkstra" or end == "Dijkstra"):
        return visualise_Dijkstra(G)
    else: 
        return visualise_biDijkstra(G, search, end)
    

def run(JSON):
    json_dict = json.loads(JSON)
    part_one = json_dict["part_one"]
    part_two = json_dict["part_two"]
    result = {
        "part_one": {
            "steps": run_algorithm(part_one),
            "path": None
        },
        "part_two": {
            "steps": run_algorithm(part_two),
            "path": None
        }
    }
    return json.dumps(result)


#endregion

window.run = run

window.python_ready()
