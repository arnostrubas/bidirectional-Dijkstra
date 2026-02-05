import networkx as nx # type: ignore
from functools import partial
from js import window # type: ignore
import json
import heapq

#region custom_classes
class Node:
    '''
    Custom class representing node of the graph.
    '''
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
    '''
    Class representing the priority queue. Uses heapq
    '''
    def __init__(self, forward = True):
        '''
        :param forward: if True, uses forward data. True by default 
        '''
        self.count = 0
        self.forward = forward

    def insert(self, element):
        '''
        inserts `element` into queue
        '''
        if (self.forward):
            heapq.heappush(self, (element.d_f, element))
        else:
            heapq.heappush(self, (element.d_b, element))
        self.count += 1

    def update(self, element):
        '''
        :param element: element which priority should be updated
        '''
        if (self.forward):
            heapq.heappush(self, (element.d_f, element))
        else:
            heapq.heappush(self, (element.d_b, element))

    def extractMin(self):
        '''
        pops the element with lowest prioriry in queue and returns it
        '''
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
    
    def min(self):
        '''
        returns priority of the element with lowest priority without removing it from the queue
        '''
        element = self.extractMin()
        self.insert(element)
        if (self.forward): return element.d_f
        else: return element.d_b
    
    def isEmpty(self):
        '''
        True if there are no elements in the queue
        '''
        return self.count == 0
    
class VisualData:
    '''
    class used for the visualisation
    '''
    def __init__(self, queue_f = Queue(), queue_b = Queue(), mu = 0):
        self.queue_f = queue_f
        self.queue_b = queue_b
        self.mu = mu

#endregion

#region json_functions
def graph_to_json(G):
    '''
    return JSON of given graph `G`
    '''
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

def queue_to_json(queue):
    '''
    converts given `queue` to JSON
    '''
    nodes = []
    for d, node in queue:
        if(queue.forward and node.d_f == d): nodes.append((d, node.id))
        if(not queue.forward and node.d_b == d): nodes.append((d, node.id))
    return json.dumps({
        "queue": nodes
    })
#endregion

#region other functions
def node_from_graph(G, id):
    '''
    returns node with `id` in graph `G`, otherwise None
    '''
    for node in G.nodes:
        if node.id == id:
            return node
    return None

def node_on_path(node):
    '''
    Changes states of `node` so it is highlighted in graph visual
    '''
    node.state_f = "PATH"
    node.state_b = "PATH"

def edge_on_path(G, id1, id2):
    '''
    changes state of edge between `id1` and `id2` so that it is highlighted in graph visual
    '''
    G[node_from_graph(G, id1)][node_from_graph(G, id2)]['state'] = "PATH"
#endregion

#region algorithms and their functions
def NCPP(G, end, v = None):
    '''
    highlights the shortest path found by (bi)directional Dijkstra
    
    :param G: graph to extract the shortest path from
    :param end: 0 for Dijkstra, 1 for same vertex closed/first encounter, 2 for search distance
    :param v: middle node, used only when end = 2, search distance
    '''
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
            
    "same vertex closed"
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
    
    "search distance"
    if end == 2:
        pred = v
        while pred is not None:
            node_on_path(pred)
            if (pred.pi_f): edge_on_path(G, pred.pi_f.id, pred.id)
            pred = pred.pi_f

        pred = v
        while pred is not None:
            node_on_path(pred)
            if (pred.pi_b): edge_on_path(G, pred.id, pred.pi_b.id)
            pred = pred.pi_b

def w_function(G, u, v):
    '''
    return weight of edge between `u` and `v` in graph `G`
    '''
    return G[u][v]['weight']

def init(G, s, t=None):
    '''
    initialises graph `G`
    
    :param s: starting node
    :param t: ending node, specify only for bidirectional search
    '''
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
    yield VisualData(queue_f=Q)
    while not Q.isEmpty():
        v = Q.extractMin()
        v.state_f = "CLOSED"
        yield VisualData(queue_f=Q)                     # for visualisation purposes
        if (v == t):
            NCPP(G, 0)
            yield VisualData(queue_f=Q)                 # for visualisation purposes
            return
        for u in sorted(G.successors(v), key=lambda node: node.id):
            if u.state_f == "UNVISITED":
                u.d_f = v.d_f + w(v, u)
                u.state_f = "OPEN"
                u.pi_f = v
                Q.insert(u)
                yield VisualData(queue_f=Q)             # for visualisation purposes
            elif u.state_f == "OPEN":
                if v.d_f + w(v, u) < u.d_f:
                    u.d_f = v.d_f + w(v, u)
                    u.pi_f = v
                    Q.update(u) 
                    yield VisualData(queue_f=Q)         # for visualisation purposes
    return None

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
    yield VisualData(queue_f=Q_f, queue_b=Q_b)                      # for visualisation purposes
    while (not Q_f.isEmpty()) and (not Q_b.isEmpty()):
        if (fwd):
            v = Q_f.extractMin()
            v.state_f = "CLOSED"
            yield VisualData(queue_f=Q_f, queue_b=Q_b)              # for visualisation purposes
            if (v.state_b == "CLOSED"):
                NCPP(G, 1)
                yield VisualData(queue_f=Q_f, queue_b=Q_b)          # for visualisation purposes
                return None                 
            for u in sorted(G.successors(v), key=lambda node: node.id):
                if u.state_f == "UNVISITED":
                    u.d_f = v.d_f + w(v, u)
                    u.state_f = "OPEN"
                    u.pi_f = v
                    Q_f.insert(u)
                    yield VisualData(queue_f=Q_f, queue_b=Q_b)      # for visualisation purposes
                elif u.state_f == "OPEN":
                    if v.d_f + w(v, u) < u.d_f:
                        u.d_f = v.d_f + w(v, u)
                        u.pi_f = v
                        Q_f.update(u) 
                        yield VisualData(queue_f=Q_f, queue_b=Q_b)  # for visualisation purposes
            fwd = not fwd
        else:
            v = Q_b.extractMin()
            v.state_b = "CLOSED"
            yield VisualData(queue_f=Q_f, queue_b=Q_b)              # for visualisation purposes
            if (v.state_f == "CLOSED"):
                NCPP(G, 1)
                yield VisualData(queue_f=Q_f, queue_b=Q_b)
                return None  
            for u in sorted(G.predecessors(v), key=lambda node: node.id):
                if u.state_b == "UNVISITED":
                    u.d_b = v.d_b + w(u, v)
                    u.state_b = "OPEN"
                    u.pi_b = v
                    Q_b.insert(u)
                    yield VisualData(queue_f=Q_f, queue_b=Q_b)     # for visualisation purposes
                elif u.state_b == "OPEN":
                    if v.d_b + w(u, v) < u.d_b:
                        u.d_b = v.d_b + w(u, v)
                        u.pi_b = v
                        Q_b.update(u) 
                        yield VisualData(queue_f=Q_f, queue_b=Q_b) # for visualisation purposes
            fwd = not fwd
    return None

def bidirectional_Dijkstra_2(G, w, s, t):
    """
    Search = after one vertex \n
    End = first encounter
    """
    init(G, s, t)
    Q_f = Queue()
    Q_f.insert(s)
    Q_b = Queue(False)
    Q_b.insert(t)
    fwd = True
    yield VisualData(queue_f=Q_f, queue_b=Q_b)                          # for visualisation purposes
    while (not Q_f.isEmpty()) and (not Q_b.isEmpty()):
        if (fwd):
            v = Q_f.extractMin()
            v.state_f = "CLOSED"
            yield VisualData(queue_f=Q_f, queue_b=Q_b)                  # for visualisation purposes               
            for u in sorted(G.successors(v), key=lambda node: node.id):
                if u.state_f == "UNVISITED":
                    u.d_f = v.d_f + w(v, u)
                    u.state_f = "OPEN"
                    u.pi_f = v
                    Q_f.insert(u)
                    yield VisualData(queue_f=Q_f, queue_b=Q_b)          # for visualisation purposes
                elif u.state_f == "OPEN":
                    if v.d_f + w(v, u) < u.d_f:
                        u.d_f = v.d_f + w(v, u)
                        u.pi_f = v
                        Q_f.update(u) 
                        yield VisualData(queue_f=Q_f, queue_b=Q_b)      # for visualisation purposes
                if (u.state_b == "OPEN" or u.state_b == "CLOSED"):
                    NCPP(G, 1)
                    yield VisualData(queue_f=Q_f, queue_b=Q_b)          # for visualisation purposes
                    return None
            fwd = not fwd
        else:
            v = Q_b.extractMin()
            v.state_b = "CLOSED"
            yield VisualData(queue_f=Q_f, queue_b=Q_b)                  # for visualisation purposes
            for u in sorted(G.predecessors(v), key=lambda node: node.id):
                if u.state_b == "UNVISITED":
                    u.d_b = v.d_b + w(u, v)
                    u.state_b = "OPEN"
                    u.pi_b = v
                    Q_b.insert(u)
                    yield VisualData(queue_f=Q_f, queue_b=Q_b)          # for visualisation purposes
                elif u.state_b == "OPEN":
                    if v.d_b + w(u, v) < u.d_b:
                        u.d_b = v.d_b + w(u, v)
                        u.pi_b = v
                        Q_b.update(u) 
                        yield VisualData(queue_f=Q_f, queue_b=Q_b)      # for visualisation purposes
                if (u.state_f == "OPEN" or u.state_f == "CLOSED"):
                    NCPP(G, 1)
                    yield VisualData(queue_f=Q_f, queue_b=Q_b)          # for visualisation purposes
                    return None
            fwd = not fwd
    return None

def bidirectional_Dijkstra_3(G, w, s, t):
    """
    Search = after one vertex \n
    End = using distance of search
    """
    init(G, s, t)
    Q_f = Queue()
    Q_f.insert(s)
    Q_b = Queue(False)
    Q_b.insert(t)
    fwd = True
    mu = 99999999999
    middle_vertex = None
    current_node_f = None
    current_node_b = None
    yield VisualData(queue_f=Q_f, queue_b=Q_b, mu=mu)                          # for visualisation purposes
    while (not Q_f.isEmpty()) and (not Q_b.isEmpty()):
        if (fwd):
            v = Q_f.extractMin()
            current_node_f = v
            v.state_f = "CLOSED"
            if (current_node_b and current_node_f and current_node_f.d_f + current_node_b.d_b > mu):
                NCPP(G, 2, middle_vertex)
                yield VisualData(queue_f=Q_f, queue_b=Q_b, mu=mu)               # for visualisation purposes
                return None
            yield VisualData(queue_f=Q_f, queue_b=Q_b, mu=mu)                   # for visualisation purposes               
            for u in sorted(G.successors(v), key=lambda node: node.id):
                if u.state_f == "UNVISITED":
                    u.d_f = v.d_f + w(v, u)
                    u.state_f = "OPEN"
                    u.pi_f = v
                    Q_f.insert(u)
                    yield VisualData(queue_f=Q_f, queue_b=Q_b, mu=mu)            # for visualisation purposes
                elif u.state_f == "OPEN":
                    if v.d_f + w(v, u) < u.d_f:
                        u.d_f = v.d_f + w(v, u)
                        u.pi_f = v
                        Q_f.update(u) 
                        yield VisualData(queue_f=Q_f, queue_b=Q_b, mu=mu)        # for visualisation purposes
                if (u.state_b == "CLOSED" and v.d_f + u.d_b + w(v, u) < mu):
                    middle_vertex = v
                    mu = v.d_f + u.d_b + w(v, u)
            fwd = not fwd
        else:
            v = Q_b.extractMin()
            current_node_b = v
            v.state_b = "CLOSED"
            if (current_node_f.d_f + current_node_b.d_b > mu):
                NCPP(G, 2, middle_vertex)
                yield VisualData(queue_f=Q_f, queue_b=Q_b, mu=mu)                # for visualisation purposes
                return None
            yield VisualData(queue_f=Q_f, queue_b=Q_b, mu=mu)                    # for visualisation purposes
            for u in sorted(G.predecessors(v), key=lambda node: node.id):
                if u.state_b == "UNVISITED":
                    u.d_b = v.d_b + w(u, v)
                    u.state_b = "OPEN"
                    u.pi_b = v
                    Q_b.insert(u)
                    yield VisualData(queue_f=Q_f, queue_b=Q_b, mu=mu)            # for visualisation purposes
                elif u.state_b == "OPEN":
                    if v.d_b + w(u, v) < u.d_b:
                        u.d_b = v.d_b + w(u, v)
                        u.pi_b = v
                        Q_b.update(u) 
                        yield VisualData(queue_f=Q_f, queue_b=Q_b, mu=mu)        # for visualisation purposes
                if (u.state_f == "CLOSED" and v.d_b + u.d_f + w(u, v) < mu):
                    middle_vertex = v
                    mu = v.d_b + u.d_f + w(u, v)
            fwd = not fwd
    return None

def bidirectional_Dijkstra_4(G, w, s, t):
    """
    Search = less open vertexes \n
    End = same vertex close
    """
    init(G, s, t)
    Q_f = Queue()
    Q_f.insert(s)
    Q_b = Queue(False)
    Q_b.insert(t)
    yield VisualData(queue_f=Q_f, queue_b=Q_b)                      # for visualisation purposes
    while (not Q_f.isEmpty()) and (not Q_b.isEmpty()):
        if (Q_f.count <= Q_b.count):
            v = Q_f.extractMin()
            v.state_f = "CLOSED"
            yield VisualData(queue_f=Q_f, queue_b=Q_b)              # for visualisation purposes
            if (v.state_b == "CLOSED"):
                NCPP(G, 1)
                yield VisualData(queue_f=Q_f, queue_b=Q_b)          # for visualisation purposes
                return None                 
            for u in sorted(G.successors(v), key=lambda node: node.id):
                if u.state_f == "UNVISITED":
                    u.d_f = v.d_f + w(v, u)
                    u.state_f = "OPEN"
                    u.pi_f = v
                    Q_f.insert(u)
                    yield VisualData(queue_f=Q_f, queue_b=Q_b)      # for visualisation purposes
                elif u.state_f == "OPEN":
                    if v.d_f + w(v, u) < u.d_f:
                        u.d_f = v.d_f + w(v, u)
                        u.pi_f = v
                        Q_f.update(u) 
                        yield VisualData(queue_f=Q_f, queue_b=Q_b)  # for visualisation purposes
        else:
            v = Q_b.extractMin()
            v.state_b = "CLOSED"
            yield VisualData(queue_f=Q_f, queue_b=Q_b)              # for visualisation purposes
            if (v.state_f == "CLOSED"):
                NCPP(G, 1)
                yield VisualData(queue_f=Q_f, queue_b=Q_b)
                return None  
            for u in sorted(G.predecessors(v), key=lambda node: node.id):
                if u.state_b == "UNVISITED":
                    u.d_b = v.d_b + w(u, v)
                    u.state_b = "OPEN"
                    u.pi_b = v
                    Q_b.insert(u)
                    yield VisualData(queue_f=Q_f, queue_b=Q_b)     # for visualisation purposes
                elif u.state_b == "OPEN":
                    if v.d_b + w(u, v) < u.d_b:
                        u.d_b = v.d_b + w(u, v)
                        u.pi_b = v
                        Q_b.update(u) 
                        yield VisualData(queue_f=Q_f, queue_b=Q_b) # for visualisation purposes
    return None

def bidirectional_Dijkstra_5(G, w, s, t):
    """
    Search = less open vertexes \n
    End = first encounter
    """
    init(G, s, t)
    Q_f = Queue()
    Q_f.insert(s)
    Q_b = Queue(False)
    Q_b.insert(t)
    yield VisualData(queue_f=Q_f, queue_b=Q_b)                          # for visualisation purposes
    while (not Q_f.isEmpty()) and (not Q_b.isEmpty()):
        if (Q_f.count <= Q_b.count):
            v = Q_f.extractMin()
            v.state_f = "CLOSED"
            yield VisualData(queue_f=Q_f, queue_b=Q_b)                  # for visualisation purposes               
            for u in sorted(G.successors(v), key=lambda node: node.id):
                if u.state_f == "UNVISITED":
                    u.d_f = v.d_f + w(v, u)
                    u.state_f = "OPEN"
                    u.pi_f = v
                    Q_f.insert(u)
                    yield VisualData(queue_f=Q_f, queue_b=Q_b)          # for visualisation purposes
                elif u.state_f == "OPEN":
                    if v.d_f + w(v, u) < u.d_f:
                        u.d_f = v.d_f + w(v, u)
                        u.pi_f = v
                        Q_f.update(u) 
                        yield VisualData(queue_f=Q_f, queue_b=Q_b)      # for visualisation purposes
                if (u.state_b == "OPEN" or u.state_b == "CLOSED"):
                    NCPP(G, 1)
                    yield VisualData(queue_f=Q_f, queue_b=Q_b)          # for visualisation purposes
                    return None
        else:
            v = Q_b.extractMin()
            v.state_b = "CLOSED"
            yield VisualData(queue_f=Q_f, queue_b=Q_b)                  # for visualisation purposes
            for u in sorted(G.predecessors(v), key=lambda node: node.id):
                if u.state_b == "UNVISITED":
                    u.d_b = v.d_b + w(u, v)
                    u.state_b = "OPEN"
                    u.pi_b = v
                    Q_b.insert(u)
                    yield VisualData(queue_f=Q_f, queue_b=Q_b)          # for visualisation purposes
                elif u.state_b == "OPEN":
                    if v.d_b + w(u, v) < u.d_b:
                        u.d_b = v.d_b + w(u, v)
                        u.pi_b = v
                        Q_b.update(u) 
                        yield VisualData(queue_f=Q_f, queue_b=Q_b)      # for visualisation purposes
                if (u.state_f == "OPEN" or u.state_f == "CLOSED"):
                    NCPP(G, 1)
                    yield VisualData(queue_f=Q_f, queue_b=Q_b)          # for visualisation purposes
                    return None
    return None

def bidirectional_Dijkstra_6(G, w, s, t):
    """
    Search = less open vertexes \n
    End = using distance of search
    """
    init(G, s, t)
    Q_f = Queue()
    Q_f.insert(s)
    Q_b = Queue(False)
    Q_b.insert(t)
    mu = 99999999999
    middle_vertex = None
    current_node_f = None
    current_node_b = None
    yield VisualData(queue_f=Q_f, queue_b=Q_b, mu=mu)                           # for visualisation purposes
    while (not Q_f.isEmpty()) and (not Q_b.isEmpty()):
        if (Q_f.count <= Q_b.count):
            v = Q_f.extractMin()
            current_node_f = v
            v.state_f = "CLOSED"
            if (current_node_b and current_node_f and current_node_f.d_f + current_node_b.d_b > mu):
                NCPP(G, 2, middle_vertex)
                yield VisualData(queue_f=Q_f, queue_b=Q_b, mu=mu)               # for visualisation purposes
                return None
            yield VisualData(queue_f=Q_f, queue_b=Q_b, mu=mu)                   # for visualisation purposes               
            for u in sorted(G.successors(v), key=lambda node: node.id):
                if u.state_f == "UNVISITED":
                    u.d_f = v.d_f + w(v, u)
                    u.state_f = "OPEN"
                    u.pi_f = v
                    Q_f.insert(u)
                    yield VisualData(queue_f=Q_f, queue_b=Q_b, mu=mu)            # for visualisation purposes
                elif u.state_f == "OPEN":
                    if v.d_f + w(v, u) < u.d_f:
                        u.d_f = v.d_f + w(v, u)
                        u.pi_f = v
                        Q_f.update(u) 
                        yield VisualData(queue_f=Q_f, queue_b=Q_b, mu=mu)        # for visualisation purposes
                if (u.state_b == "CLOSED" and v.d_f + u.d_b + w(v, u) < mu):
                    middle_vertex = v
                    mu = v.d_f + u.d_b + w(v, u)
        else:
            v = Q_b.extractMin()
            current_node_b = v
            v.state_b = "CLOSED"
            if (current_node_f.d_f + current_node_b.d_b > mu):
                NCPP(G, 2, middle_vertex)
                yield VisualData(queue_f=Q_f, queue_b=Q_b, mu=mu)                # for visualisation purposes
                return None
            yield VisualData(queue_f=Q_f, queue_b=Q_b, mu=mu)                    # for visualisation purposes
            for u in sorted(G.predecessors(v), key=lambda node: node.id):
                if u.state_b == "UNVISITED":
                    u.d_b = v.d_b + w(u, v)
                    u.state_b = "OPEN"
                    u.pi_b = v
                    Q_b.insert(u)
                    yield VisualData(queue_f=Q_f, queue_b=Q_b, mu=mu)            # for visualisation purposes
                elif u.state_b == "OPEN":
                    if v.d_b + w(u, v) < u.d_b:
                        u.d_b = v.d_b + w(u, v)
                        u.pi_b = v
                        Q_b.update(u) 
                        yield VisualData(queue_f=Q_f, queue_b=Q_b, mu=mu)        # for visualisation purposes
                if (u.state_f == "CLOSED" and v.d_b + u.d_f + w(u, v) < mu):
                    middle_vertex = v
                    mu = v.d_b + u.d_f + w(u, v)
    return None

def bidirectional_Dijkstra_7(G, w, s, t):
    """
    Search = lower queue priority \n
    End = same vertex close
    """
    init(G, s, t)
    Q_f = Queue()
    Q_f.insert(s)
    Q_b = Queue(False)
    Q_b.insert(t)
    yield VisualData(queue_f=Q_f, queue_b=Q_b)                      # for visualisation purposes
    while (not Q_f.isEmpty()) and (not Q_b.isEmpty()):
        if (Q_f.min() <= Q_b.min()):
            v = Q_f.extractMin()
            v.state_f = "CLOSED"
            yield VisualData(queue_f=Q_f, queue_b=Q_b)              # for visualisation purposes
            if (v.state_b == "CLOSED"):
                NCPP(G, 1)
                yield VisualData(queue_f=Q_f, queue_b=Q_b)          # for visualisation purposes
                return None                 
            for u in sorted(G.successors(v), key=lambda node: node.id):
                if u.state_f == "UNVISITED":
                    u.d_f = v.d_f + w(v, u)
                    u.state_f = "OPEN"
                    u.pi_f = v
                    Q_f.insert(u)
                    yield VisualData(queue_f=Q_f, queue_b=Q_b)      # for visualisation purposes
                elif u.state_f == "OPEN":
                    if v.d_f + w(v, u) < u.d_f:
                        u.d_f = v.d_f + w(v, u)
                        u.pi_f = v
                        Q_f.update(u) 
                        yield VisualData(queue_f=Q_f, queue_b=Q_b)  # for visualisation purposes
        else:
            v = Q_b.extractMin()
            v.state_b = "CLOSED"
            yield VisualData(queue_f=Q_f, queue_b=Q_b)              # for visualisation purposes
            if (v.state_f == "CLOSED"):
                NCPP(G, 1)
                yield VisualData(queue_f=Q_f, queue_b=Q_b)
                return None  
            for u in sorted(G.predecessors(v), key=lambda node: node.id):
                if u.state_b == "UNVISITED":
                    u.d_b = v.d_b + w(u, v)
                    u.state_b = "OPEN"
                    u.pi_b = v
                    Q_b.insert(u)
                    yield VisualData(queue_f=Q_f, queue_b=Q_b)     # for visualisation purposes
                elif u.state_b == "OPEN":
                    if v.d_b + w(u, v) < u.d_b:
                        u.d_b = v.d_b + w(u, v)
                        u.pi_b = v
                        Q_b.update(u) 
                        yield VisualData(queue_f=Q_f, queue_b=Q_b) # for visualisation purposes
    return None

def bidirectional_Dijkstra_8(G, w, s, t):
    """
    Search = lower queue priority \n
    End = first encounter
    """
    init(G, s, t)
    Q_f = Queue()
    Q_f.insert(s)
    Q_b = Queue(False)
    Q_b.insert(t)
    yield VisualData(queue_f=Q_f, queue_b=Q_b)                          # for visualisation purposes
    while (not Q_f.isEmpty()) and (not Q_b.isEmpty()):
        if (Q_f.min() <= Q_b.min()):
            v = Q_f.extractMin()
            v.state_f = "CLOSED"
            yield VisualData(queue_f=Q_f, queue_b=Q_b)                  # for visualisation purposes               
            for u in sorted(G.successors(v), key=lambda node: node.id):
                if u.state_f == "UNVISITED":
                    u.d_f = v.d_f + w(v, u)
                    u.state_f = "OPEN"
                    u.pi_f = v
                    Q_f.insert(u)
                    yield VisualData(queue_f=Q_f, queue_b=Q_b)          # for visualisation purposes
                elif u.state_f == "OPEN":
                    if v.d_f + w(v, u) < u.d_f:
                        u.d_f = v.d_f + w(v, u)
                        u.pi_f = v
                        Q_f.update(u) 
                        yield VisualData(queue_f=Q_f, queue_b=Q_b)      # for visualisation purposes
                if (u.state_b == "OPEN" or u.state_b == "CLOSED"):
                    NCPP(G, 1)
                    yield VisualData(queue_f=Q_f, queue_b=Q_b)          # for visualisation purposes
                    return None
        else:
            v = Q_b.extractMin()
            v.state_b = "CLOSED"
            yield VisualData(queue_f=Q_f, queue_b=Q_b)                  # for visualisation purposes
            for u in sorted(G.predecessors(v), key=lambda node: node.id):
                if u.state_b == "UNVISITED":
                    u.d_b = v.d_b + w(u, v)
                    u.state_b = "OPEN"
                    u.pi_b = v
                    Q_b.insert(u)
                    yield VisualData(queue_f=Q_f, queue_b=Q_b)          # for visualisation purposes
                elif u.state_b == "OPEN":
                    if v.d_b + w(u, v) < u.d_b:
                        u.d_b = v.d_b + w(u, v)
                        u.pi_b = v
                        Q_b.update(u) 
                        yield VisualData(queue_f=Q_f, queue_b=Q_b)      # for visualisation purposes
                if (u.state_f == "OPEN" or u.state_f == "CLOSED"):
                    NCPP(G, 1)
                    yield VisualData(queue_f=Q_f, queue_b=Q_b)          # for visualisation purposes
                    return None
    return None

def bidirectional_Dijkstra_9(G, w, s, t):
    """
    Search = lower queue priority \n
    End = using distance of search
    """
    init(G, s, t)
    Q_f = Queue()
    Q_f.insert(s)
    Q_b = Queue(False)
    Q_b.insert(t)
    mu = 99999999999
    middle_vertex = None
    current_node_f = None
    current_node_b = None
    yield VisualData(queue_f=Q_f, queue_b=Q_b, mu=mu)                           # for visualisation purposes
    while (not Q_f.isEmpty()) and (not Q_b.isEmpty()):
        if (Q_f.min() <= Q_b.min()):
            v = Q_f.extractMin()
            current_node_f = v
            v.state_f = "CLOSED"
            if (current_node_b and current_node_f and current_node_f.d_f + current_node_b.d_b > mu):
                NCPP(G, 2, middle_vertex)
                yield VisualData(queue_f=Q_f, queue_b=Q_b, mu=mu)               # for visualisation purposes
                return None
            yield VisualData(queue_f=Q_f, queue_b=Q_b, mu=mu)                   # for visualisation purposes               
            for u in sorted(G.successors(v), key=lambda node: node.id):
                if u.state_f == "UNVISITED":
                    u.d_f = v.d_f + w(v, u)
                    u.state_f = "OPEN"
                    u.pi_f = v
                    Q_f.insert(u)
                    yield VisualData(queue_f=Q_f, queue_b=Q_b, mu=mu)            # for visualisation purposes
                elif u.state_f == "OPEN":
                    if v.d_f + w(v, u) < u.d_f:
                        u.d_f = v.d_f + w(v, u)
                        u.pi_f = v
                        Q_f.update(u) 
                        yield VisualData(queue_f=Q_f, queue_b=Q_b, mu=mu)        # for visualisation purposes
                if (u.state_b == "CLOSED" and v.d_f + u.d_b + w(v, u) < mu):
                    middle_vertex = v
                    mu = v.d_f + u.d_b + w(v, u)
        else:
            v = Q_b.extractMin()
            current_node_b = v
            v.state_b = "CLOSED"
            if (current_node_f.d_f + current_node_b.d_b > mu):
                NCPP(G, 2, middle_vertex)
                yield VisualData(queue_f=Q_f, queue_b=Q_b, mu=mu)                # for visualisation purposes
                return None
            yield VisualData(queue_f=Q_f, queue_b=Q_b, mu=mu)                    # for visualisation purposes
            for u in sorted(G.predecessors(v), key=lambda node: node.id):
                if u.state_b == "UNVISITED":
                    u.d_b = v.d_b + w(u, v)
                    u.state_b = "OPEN"
                    u.pi_b = v
                    Q_b.insert(u)
                    yield VisualData(queue_f=Q_f, queue_b=Q_b, mu=mu)            # for visualisation purposes
                elif u.state_b == "OPEN":
                    if v.d_b + w(u, v) < u.d_b:
                        u.d_b = v.d_b + w(u, v)
                        u.pi_b = v
                        Q_b.update(u) 
                        yield VisualData(queue_f=Q_f, queue_b=Q_b, mu=mu)        # for visualisation purposes
                if (u.state_f == "CLOSED" and v.d_b + u.d_f + w(u, v) < mu):
                    middle_vertex = v
                    mu = v.d_b + u.d_f + w(u, v)
    return None

def bidirectional_Dijkstra_10(G, w, s, t):
    """
    Search = after one edge \n
    End = same vertex close
    """
    def forward_one_edge(G, Q_f):
        while (not Q_f.isEmpty()):
            v = Q_f.extractMin()
            v.state_f = "CLOSED"
            yield True
            if (v.state_b == "CLOSED"):
                NCPP(G, 1)
                yield False
                return None                 
            for u in sorted(G.successors(v), key=lambda node: node.id):
                if u.state_f == "UNVISITED":
                    u.d_f = v.d_f + w(v, u)
                    u.state_f = "OPEN"
                    u.pi_f = v
                    Q_f.insert(u)
                    yield False
                elif u.state_f == "OPEN":
                    if v.d_f + w(v, u) < u.d_f:
                        u.d_f = v.d_f + w(v, u)
                        u.pi_f = v
                        Q_f.update(u) 
                        yield False
    
    def backward_one_edge(G, Q_b):
        while (not Q_b.isEmpty()):
            v = Q_b.extractMin()
            v.state_b = "CLOSED"
            yield True
            if (v.state_f == "CLOSED"):
                NCPP(G, 1)
                yield False
                return None  
            for u in sorted(G.predecessors(v), key=lambda node: node.id):
                if u.state_b == "UNVISITED":
                    u.d_b = v.d_b + w(u, v)
                    u.state_b = "OPEN"
                    u.pi_b = v
                    Q_b.insert(u)
                    yield False
                elif u.state_b == "OPEN":
                    if v.d_b + w(u, v) < u.d_b:
                        u.d_b = v.d_b + w(u, v)
                        u.pi_b = v
                        Q_b.update(u) 
                        yield False

    init(G, s, t)
    Q_f = Queue()
    Q_f.insert(s)
    Q_b = Queue(False)
    Q_b.insert(t)
    fwd = True
    yield VisualData(queue_f=Q_f, queue_b=Q_b)              # for visualisation purposes
    fwd_runner = forward_one_edge(G, Q_f)
    bck_runner = backward_one_edge(G, Q_b)
    while (not Q_f.isEmpty()) and (not Q_b.isEmpty()):
        if (fwd):
            try:
                if (next(fwd_runner)): 
                    yield VisualData(queue_f=Q_f, queue_b=Q_b)  # for visualisation purposes
                    next(fwd_runner)
                yield VisualData(queue_f=Q_f, queue_b=Q_b)      # for visualisation purposes
            except StopIteration:
                return None
        else:
            try:
                if (next(bck_runner)): 
                    yield VisualData(queue_f=Q_f, queue_b=Q_b)  # for visualisation purposes
                    next(bck_runner)
                yield VisualData(queue_f=Q_f, queue_b=Q_b)      # for visualisation purposes
            except StopIteration:
                return None
        fwd = not fwd
            
    return None

def bidirectional_Dijkstra_11(G, w, s, t):
    """
    Search = after one edge \n
    End = first encounter
    """
    def forward_one_edge(G, Q_f):
        while (not Q_f.isEmpty()):
            v = Q_f.extractMin()
            v.state_f = "CLOSED"
            yield True                
            for u in sorted(G.successors(v), key=lambda node: node.id):
                if u.state_f == "UNVISITED":
                    u.d_f = v.d_f + w(v, u)
                    u.state_f = "OPEN"
                    u.pi_f = v
                    Q_f.insert(u)
                    yield False
                elif u.state_f == "OPEN":
                    if v.d_f + w(v, u) < u.d_f:
                        u.d_f = v.d_f + w(v, u)
                        u.pi_f = v
                        Q_f.update(u) 
                        yield False
                if (u.state_b == "OPEN" or u.state_b == "CLOSED"):
                    NCPP(G, 1)
                    yield VisualData(queue_f=Q_f, queue_b=Q_b)          # for visualisation purposes
                    return None
    
    def backward_one_edge(G, Q_b):
        while (not Q_b.isEmpty()):
            v = Q_b.extractMin()
            v.state_b = "CLOSED"
            yield True
            for u in sorted(G.predecessors(v), key=lambda node: node.id):
                if u.state_b == "UNVISITED":
                    u.d_b = v.d_b + w(u, v)
                    u.state_b = "OPEN"
                    u.pi_b = v
                    Q_b.insert(u)
                    yield False
                elif u.state_b == "OPEN":
                    if v.d_b + w(u, v) < u.d_b:
                        u.d_b = v.d_b + w(u, v)
                        u.pi_b = v
                        Q_b.update(u) 
                        yield False
                if (u.state_f == "OPEN" or u.state_f == "CLOSED"):
                    NCPP(G, 1)
                    yield VisualData(queue_f=Q_f, queue_b=Q_b)          # for visualisation purposes
                    return None

    init(G, s, t)
    Q_f = Queue()
    Q_f.insert(s)
    Q_b = Queue(False)
    Q_b.insert(t)
    fwd = True
    yield VisualData(queue_f=Q_f, queue_b=Q_b)              # for visualisation purposes
    fwd_runner = forward_one_edge(G, Q_f)
    bck_runner = backward_one_edge(G, Q_b)
    while (not Q_f.isEmpty()) and (not Q_b.isEmpty()):
        if (fwd):
            try:
                if (next(fwd_runner)): 
                    yield VisualData(queue_f=Q_f, queue_b=Q_b)  # for visualisation purposes
                    next(fwd_runner)
                yield VisualData(queue_f=Q_f, queue_b=Q_b)      # for visualisation purposes
            except StopIteration:
                return None
        else:
            try:
                if (next(bck_runner)): 
                    yield VisualData(queue_f=Q_f, queue_b=Q_b)  # for visualisation purposes
                    next(bck_runner)
                yield VisualData(queue_f=Q_f, queue_b=Q_b)      # for visualisation purposes
            except StopIteration:
                return None
        fwd = not fwd
            
    return None

def bidirectional_Dijkstra_12(G, w, s, t):
    """
    Search = after one edge \n
    End = using search distance
    """
    mu = 99999999999
    middle_vertex = None
    current_node_f = None
    current_node_b = None

    '''
    next two functions yield True when one neighbour has been explored. 
    yield False is only for visual purposes
    '''
    def forward_one_edge(G, Q_f):
        nonlocal mu, middle_vertex, current_node_b, current_node_f
        while (not Q_f.isEmpty()):
            v = Q_f.extractMin()
            v.state_f = "CLOSED"
            current_node_f = v
            yield False   
            if (current_node_b and current_node_f and current_node_f.d_f + current_node_b.d_b > mu):
                NCPP(G, 2, middle_vertex)
                yield False               
                return None             
            for u in sorted(G.successors(v), key=lambda node: node.id):
                if u.state_f == "UNVISITED":
                    u.d_f = v.d_f + w(v, u)
                    u.state_f = "OPEN"
                    u.pi_f = v
                    Q_f.insert(u)
                    yield True
                elif u.state_f == "OPEN":
                    if v.d_f + w(v, u) < u.d_f:
                        u.d_f = v.d_f + w(v, u)
                        u.pi_f = v
                        Q_f.update(u) 
                        yield True
                if (u.state_b == "CLOSED" and v.d_f + u.d_b + w(v, u) < mu):
                    middle_vertex = v
                    mu = v.d_f + u.d_b + w(v, u)
        return None
    
    def backward_one_edge(G, Q_b):
        nonlocal mu, middle_vertex, current_node_b, current_node_f
        while (not Q_b.isEmpty()):
            v = Q_b.extractMin()
            v.state_b = "CLOSED"
            current_node_b = v
            yield False
            if (current_node_b and current_node_f and current_node_f.d_f + current_node_b.d_b > mu):
                NCPP(G, 2, middle_vertex)
                yield False          
                return None
            for u in sorted(G.predecessors(v), key=lambda node: node.id):
                if u.state_b == "UNVISITED":
                    u.d_b = v.d_b + w(u, v)
                    u.state_b = "OPEN"
                    u.pi_b = v
                    Q_b.insert(u)
                    yield True
                elif u.state_b == "OPEN":
                    if v.d_b + w(u, v) < u.d_b:
                        u.d_b = v.d_b + w(u, v)
                        u.pi_b = v
                        Q_b.update(u) 
                        yield True
                if (u.state_f == "CLOSED" and v.d_b + u.d_f + w(u, v) < mu):
                    middle_vertex = v
                    mu = v.d_b + u.d_f + w(u, v)
        return None

    init(G, s, t)
    Q_f = Queue()
    Q_f.insert(s)
    Q_b = Queue(False)
    Q_b.insert(t)
    fwd = True
    yield VisualData(queue_f=Q_f, queue_b=Q_b)              # for visualisation purposes
    fwd_runner = forward_one_edge(G, Q_f)
    bck_runner = backward_one_edge(G, Q_b)
    while (not Q_f.isEmpty()) and (not Q_b.isEmpty()):
        if (fwd):
            try:
                while(not next(fwd_runner)):    
                    'explores one neighbour. Multiple steps are only neccessary for visual purposes'                
                    yield VisualData(queue_f=Q_f, queue_b=Q_b)
                yield VisualData(queue_f=Q_f, queue_b=Q_b)
            except StopIteration:                               # means the runner returned None
                return None
        else:
            try:
                while(not next(bck_runner)):
                    'explores one neighbour. Multiple steps are only neccessary for visual purposes'                        
                    yield VisualData(queue_f=Q_f, queue_b=Q_b)
                yield VisualData(queue_f=Q_f, queue_b=Q_b) 
            except StopIteration:                               # means the runner returned None
                return None
        fwd = not fwd
            
    return None
#endregion

#region visualisation functions
def visualise_algorithm(G, search, end):
    '''
    visualises algorithm with `search` and `end` strategies on graph `G`

    returns json with graph, queue and other data
    '''
    s = node_from_graph(G, -1) 
    t = node_from_graph(G, 0)
    w = partial(w_function, G)
    match (search, end):
        case ("one_vertex", "same_vertex_closed"):
            runner = bidirectional_Dijkstra_1(G, w, s, t)
        case ("one_vertex", "first_encounter"):
            runner = bidirectional_Dijkstra_2(G, w, s, t)
        case ("one_vertex", "using_search_distance"):
            runner = bidirectional_Dijkstra_3(G, w, s, t)
        case ("less_open_vertexes", "same_vertex_closed"):
            runner = bidirectional_Dijkstra_4(G, w, s, t)
        case ("less_open_vertexes", "first_encounter"):
            runner = bidirectional_Dijkstra_5(G, w, s, t)
        case ("less_open_vertexes", "using_search_distance"):
            runner = bidirectional_Dijkstra_6(G, w, s, t)
        case ("lower_queue_priority", "same_vertex_closed"):
            runner = bidirectional_Dijkstra_7(G, w, s, t)
        case ("lower_queue_priority", "first_encounter"):
            runner = bidirectional_Dijkstra_8(G, w, s, t)
        case ("lower_queue_priority", "using_search_distance"):
            runner = bidirectional_Dijkstra_9(G, w, s, t)
        case ("one_edge", "same_vertex_closed"):
            runner = bidirectional_Dijkstra_10(G, w, s, t)
        case ("one_edge", "first_encounter"):
            runner = bidirectional_Dijkstra_11(G, w, s, t)
        case ("one_edge", "using_search_distance"):
            runner = bidirectional_Dijkstra_12(G, w, s, t)
        case _:
            runner = Dijkstra(G, w, s, t)
    result = []
    for yielded in runner:
        data = {
            "graph": graph_to_json(G),
            "queue_f": queue_to_json(yielded.queue_f),
            "queue_b": queue_to_json(yielded.queue_b),
            "mu": str(yielded.mu)
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
    
    return visualise_algorithm(G, search, end)
    
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

#allows run to be accessed from JavaScript
window.run = run

window.python_ready()
