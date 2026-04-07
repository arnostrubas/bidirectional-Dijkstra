# Copyright (c) 2026, Arnošt Rubáš
# All rights reserved.
# 
# This source code is licensed under the BSD 3-Clause License.
# The full text of the license can be found in the LICENSE file 
# in the root directory of this project.

from custom_classes import Queue
import math

def node_from_graph(G, id):
    '''
    returns node with `id` in graph `G`, otherwise None
    '''
    index = G.graph.get('nodes_by_id', {})
    return index.get(id)

def w_function(G, u, v):
    '''
    return weight of edge between `u` and `v` in graph `G`
    '''
    return G[u][v]['weight']

def ExtractShortestPath(G, end, v = None):
    '''
    highlights the shortest path found by (bi)directional Dijkstra
    
    :param G: graph to extract the shortest path from
    :param end: 0 for Dijkstra, 1 for other
    :param v: middle node or t in case of dijkstra
    '''
    path = []
    "Dijkstra"
    if end == 0: 
        path.append(v)
        node = v.pi_f
        while node is not None:
            path.append(node)
            node = node.pi_f
        path.reverse()
       
            
    "same vertex closed || search distance"
    if end == 1:
        fwd_path = []
        bwd_path = []
        pred = v
        while pred is not None:
            fwd_path.append(pred)
            pred = pred.pi_f

        pred = v.pi_b
        while pred is not None:
            bwd_path.append(pred)
            pred = pred.pi_b
        fwd_path.reverse()
        path.extend(fwd_path)
        path.extend(bwd_path)

    return path

def init(G, s, t=None):
    '''
    initialises graph `G`
    
    :param s: starting node
    :param t: ending node, specify only for bidirectional search
    '''
    for node in G.nodes:
        node.d_f = math.inf
        node.pi_f = None
        node.state_f = "UNVISITED"
        node.d_b = math.inf
        node.pi_b = None
        node.state_b = "UNVISITED"
    s.d_f = 0
    s.state_f = "OPEN"
    if (t):
        t.d_b = 0
        t.state_b = "OPEN"

def FindMinDistVertex(G):
    minimum = math.inf
    x = None
    for node in G.nodes:
        if node.d_f + node.d_b < minimum:
            minimum = node.d_f + node.d_b
            x = node
    return x

def Dijkstra(G, w, s, t):
    init(G, s)
    Q = Queue()
    Q.insert(s)
    while not Q.isEmpty():
        v = Q.extractMin()
        v.state_f = "CLOSED"
        if (v == t):
            return (t.d_f, ExtractShortestPath(G, 0, t))
        for u in sorted(G.successors(v), key=lambda node: node.id):
            if u.state_f == "UNVISITED":
                u.d_f = v.d_f + w(v, u)
                u.state_f = "OPEN"
                u.pi_f = v
                Q.insert(u)
            elif u.state_f == "OPEN":
                if v.d_f + w(v, u) < u.d_f:
                    u.d_f = v.d_f + w(v, u)
                    u.pi_f = v
                    Q.update(u) 
    return (math.inf, None)

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
    while (not Q_f.isEmpty()) and (not Q_b.isEmpty()):
        if (fwd):
            v = Q_f.extractMin()
            v.state_f = "CLOSED"
            if (v.state_b == "CLOSED"):
                u_min = FindMinDistVertex(G)
                return (u_min.d_f + u_min.d_b, ExtractShortestPath(G, 1, u_min))                
            for u in sorted(G.successors(v), key=lambda node: node.id):
                if u.state_f == "UNVISITED":
                    u.d_f = v.d_f + w(v, u)
                    u.state_f = "OPEN"
                    u.pi_f = v
                    Q_f.insert(u)
                elif u.state_f == "OPEN":
                    if v.d_f + w(v, u) < u.d_f:
                        u.d_f = v.d_f + w(v, u)
                        u.pi_f = v
                        Q_f.update(u) 
            fwd = not fwd
        else:
            v = Q_b.extractMin()
            v.state_b = "CLOSED"
            if (v.state_f == "CLOSED"):
                u_min = FindMinDistVertex(G)
                return (u_min.d_f + u_min.d_b, ExtractShortestPath(G, 1, u_min))   
            for u in sorted(G.predecessors(v), key=lambda node: node.id):
                if u.state_b == "UNVISITED":
                    u.d_b = v.d_b + w(u, v)
                    u.state_b = "OPEN"
                    u.pi_b = v
                    Q_b.insert(u)
                elif u.state_b == "OPEN":
                    if v.d_b + w(u, v) < u.d_b:
                        u.d_b = v.d_b + w(u, v)
                        u.pi_b = v
                        Q_b.update(u) 
            fwd = not fwd
    return (math.inf, None)

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
    while (not Q_f.isEmpty()) and (not Q_b.isEmpty()):
        if (fwd):
            v = Q_f.extractMin()
            v.state_f = "CLOSED"             
            for u in sorted(G.successors(v), key=lambda node: node.id):
                if u.state_f == "UNVISITED":
                    u.d_f = v.d_f + w(v, u)
                    u.state_f = "OPEN"
                    u.pi_f = v
                    Q_f.insert(u)
                elif u.state_f == "OPEN":
                    if v.d_f + w(v, u) < u.d_f:
                        u.d_f = v.d_f + w(v, u)
                        u.pi_f = v
                        Q_f.update(u) 
                if (u.state_b == "OPEN" or u.state_b == "CLOSED"):
                    return (u.d_f + u.d_b, ExtractShortestPath(G, 1, u))
            fwd = not fwd
        else:
            v = Q_b.extractMin()
            v.state_b = "CLOSED"
            for u in sorted(G.predecessors(v), key=lambda node: node.id):
                if u.state_b == "UNVISITED":
                    u.d_b = v.d_b + w(u, v)
                    u.state_b = "OPEN"
                    u.pi_b = v
                    Q_b.insert(u)
                elif u.state_b == "OPEN":
                    if v.d_b + w(u, v) < u.d_b:
                        u.d_b = v.d_b + w(u, v)
                        u.pi_b = v
                        Q_b.update(u) 
                if (u.state_f == "OPEN" or u.state_f == "CLOSED"):
                    return (u.d_f + u.d_b, ExtractShortestPath(G, 1, u))
            fwd = not fwd
    return (math.inf, None) 

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
    mu = math.inf
    middle_vertex = None
    current_node_f = None
    current_node_b = None
    while (not Q_f.isEmpty()) and (not Q_b.isEmpty()):
        if (fwd):
            v = Q_f.extractMin()
            current_node_f = v
            v.state_f = "CLOSED"
            if (current_node_b and current_node_f and current_node_f.d_f + current_node_b.d_b >= mu):
                return (mu, ExtractShortestPath(G, 1, middle_vertex))         
            for u in sorted(G.successors(v), key=lambda node: node.id):
                if u.state_f == "UNVISITED":
                    u.d_f = v.d_f + w(v, u)
                    u.state_f = "OPEN"
                    u.pi_f = v
                    Q_f.insert(u)
                elif u.state_f == "OPEN":
                    if v.d_f + w(v, u) < u.d_f:
                        u.d_f = v.d_f + w(v, u)
                        u.pi_f = v
                        Q_f.update(u) 
                if (u.state_b == "CLOSED" and v.d_f + u.d_b + w(v, u) < mu):
                    middle_vertex = v
                    mu = v.d_f + u.d_b + w(v, u)
            fwd = not fwd
        else:
            v = Q_b.extractMin()
            current_node_b = v
            v.state_b = "CLOSED"
            if (current_node_f.d_f + current_node_b.d_b > mu):
                return (mu, ExtractShortestPath(G, 1, middle_vertex))            
            for u in sorted(G.predecessors(v), key=lambda node: node.id):
                if u.state_b == "UNVISITED":
                    u.d_b = v.d_b + w(u, v)
                    u.state_b = "OPEN"
                    u.pi_b = v
                    Q_b.insert(u)
                elif u.state_b == "OPEN":
                    if v.d_b + w(u, v) < u.d_b:
                        u.d_b = v.d_b + w(u, v)
                        u.pi_b = v
                        Q_b.update(u) 
                if (u.state_f == "CLOSED" and v.d_b + u.d_f + w(u, v) < mu):
                    middle_vertex = v
                    mu = v.d_b + u.d_f + w(u, v)
            fwd = not fwd
    if middle_vertex:
        return (mu, ExtractShortestPath(G, 1, middle_vertex))   
    return (math.inf, None)

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
    did_fwd = False
    did_bwd = False
    while (not Q_f.isEmpty()) and (not Q_b.isEmpty()):
        if (not did_fwd or (did_bwd and Q_f.count <= Q_b.count)):
            did_fwd = True
            v = Q_f.extractMin()
            v.state_f = "CLOSED"
            if (v.state_b == "CLOSED"):
                u_min = FindMinDistVertex(G)
                return (u_min.d_f + u_min.d_b, ExtractShortestPath(G, 1, u_min))                
            for u in sorted(G.successors(v), key=lambda node: node.id):
                if u.state_f == "UNVISITED":
                    u.d_f = v.d_f + w(v, u)
                    u.state_f = "OPEN"
                    u.pi_f = v
                    Q_f.insert(u)
                elif u.state_f == "OPEN":
                    if v.d_f + w(v, u) < u.d_f:
                        u.d_f = v.d_f + w(v, u)
                        u.pi_f = v
                        Q_f.update(u) 
        else:
            did_bwd = True
            v = Q_b.extractMin()
            v.state_b = "CLOSED"
            if (v.state_f == "CLOSED"):
                u_min = FindMinDistVertex(G)
                return (u_min.d_f + u_min.d_b, ExtractShortestPath(G, 1, u_min)) 
            for u in sorted(G.predecessors(v), key=lambda node: node.id):
                if u.state_b == "UNVISITED":
                    u.d_b = v.d_b + w(u, v)
                    u.state_b = "OPEN"
                    u.pi_b = v
                    Q_b.insert(u)
                elif u.state_b == "OPEN":
                    if v.d_b + w(u, v) < u.d_b:
                        u.d_b = v.d_b + w(u, v)
                        u.pi_b = v
                        Q_b.update(u) 
    return (math.inf, None)

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
    did_fwd = False
    did_bwd = False
    while (not Q_f.isEmpty()) and (not Q_b.isEmpty()):
        if (not did_fwd or (did_bwd and Q_f.count <= Q_b.count)):
            did_fwd = True
            v = Q_f.extractMin()
            v.state_f = "CLOSED"              
            for u in sorted(G.successors(v), key=lambda node: node.id):
                if u.state_f == "UNVISITED":
                    u.d_f = v.d_f + w(v, u)
                    u.state_f = "OPEN"
                    u.pi_f = v
                    Q_f.insert(u)
                elif u.state_f == "OPEN":
                    if v.d_f + w(v, u) < u.d_f:
                        u.d_f = v.d_f + w(v, u)
                        u.pi_f = v
                        Q_f.update(u) 
                if (u.state_b == "OPEN" or u.state_b == "CLOSED"):
                    return (u.d_f + u.d_b, ExtractShortestPath(G, 1, u))
        else:
            did_bwd = True
            v = Q_b.extractMin()
            v.state_b = "CLOSED"
            for u in sorted(G.predecessors(v), key=lambda node: node.id):
                if u.state_b == "UNVISITED":
                    u.d_b = v.d_b + w(u, v)
                    u.state_b = "OPEN"
                    u.pi_b = v
                    Q_b.insert(u)
                elif u.state_b == "OPEN":
                    if v.d_b + w(u, v) < u.d_b:
                        u.d_b = v.d_b + w(u, v)
                        u.pi_b = v
                        Q_b.update(u) 
                if (u.state_f == "OPEN" or u.state_f == "CLOSED"):
                    return (u.d_f + u.d_b, ExtractShortestPath(G, 1, u))
    return (math.inf, None)

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
    mu = math.inf
    middle_vertex = None
    current_node_f = None
    current_node_b = None
    did_fwd = False
    did_bwd = False
    while (not Q_f.isEmpty()) and (not Q_b.isEmpty()):
        if (not did_fwd or (did_bwd and Q_f.count <= Q_b.count)):
            did_fwd = True
            v = Q_f.extractMin()
            current_node_f = v
            v.state_f = "CLOSED"
            if (current_node_b and current_node_f and current_node_f.d_f + current_node_b.d_b >= mu):
                return (mu, ExtractShortestPath(G, 1, middle_vertex))             
            for u in sorted(G.successors(v), key=lambda node: node.id):
                if u.state_f == "UNVISITED":
                    u.d_f = v.d_f + w(v, u)
                    u.state_f = "OPEN"
                    u.pi_f = v
                    Q_f.insert(u)
                elif u.state_f == "OPEN":
                    if v.d_f + w(v, u) < u.d_f:
                        u.d_f = v.d_f + w(v, u)
                        u.pi_f = v
                        Q_f.update(u) 
                if (u.state_b == "CLOSED" and v.d_f + u.d_b + w(v, u) < mu):
                    middle_vertex = v
                    mu = v.d_f + u.d_b + w(v, u)
        else:
            did_bwd = True
            v = Q_b.extractMin()
            current_node_b = v
            v.state_b = "CLOSED"
            if (current_node_f.d_f + current_node_b.d_b > mu):
                return (mu, ExtractShortestPath(G, 1, middle_vertex))
            for u in sorted(G.predecessors(v), key=lambda node: node.id):
                if u.state_b == "UNVISITED":
                    u.d_b = v.d_b + w(u, v)
                    u.state_b = "OPEN"
                    u.pi_b = v
                    Q_b.insert(u)
                elif u.state_b == "OPEN":
                    if v.d_b + w(u, v) < u.d_b:
                        u.d_b = v.d_b + w(u, v)
                        u.pi_b = v
                        Q_b.update(u) 
                if (u.state_f == "CLOSED" and v.d_b + u.d_f + w(u, v) < mu):
                    middle_vertex = v
                    mu = v.d_b + u.d_f + w(u, v)
    if middle_vertex:
        return (mu, ExtractShortestPath(G, 1, middle_vertex))
    return (math.inf, None)

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
    while (not Q_f.isEmpty()) and (not Q_b.isEmpty()):
        if (Q_f.min() <= Q_b.min()):
            v = Q_f.extractMin()
            v.state_f = "CLOSED"
            if (v.state_b == "CLOSED"):
                u_min = FindMinDistVertex(G)
                return (u_min.d_f + u_min.d_b, ExtractShortestPath(G, 1, u_min))                  
            for u in sorted(G.successors(v), key=lambda node: node.id):
                if u.state_f == "UNVISITED":
                    u.d_f = v.d_f + w(v, u)
                    u.state_f = "OPEN"
                    u.pi_f = v
                    Q_f.insert(u)
                elif u.state_f == "OPEN":
                    if v.d_f + w(v, u) < u.d_f:
                        u.d_f = v.d_f + w(v, u)
                        u.pi_f = v
                        Q_f.update(u) 
        else:
            v = Q_b.extractMin()
            v.state_b = "CLOSED"
            if (v.state_f == "CLOSED"):
                u_min = FindMinDistVertex(G)
                return (u_min.d_f + u_min.d_b, ExtractShortestPath(G, 1, u_min))   
            for u in sorted(G.predecessors(v), key=lambda node: node.id):
                if u.state_b == "UNVISITED":
                    u.d_b = v.d_b + w(u, v)
                    u.state_b = "OPEN"
                    u.pi_b = v
                    Q_b.insert(u)
                elif u.state_b == "OPEN":
                    if v.d_b + w(u, v) < u.d_b:
                        u.d_b = v.d_b + w(u, v)
                        u.pi_b = v
                        Q_b.update(u) 
    return (math.inf, None)

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
    while (not Q_f.isEmpty()) and (not Q_b.isEmpty()):
        if (Q_f.min() <= Q_b.min()):
            v = Q_f.extractMin()
            v.state_f = "CLOSED"             
            for u in sorted(G.successors(v), key=lambda node: node.id):
                if u.state_f == "UNVISITED":
                    u.d_f = v.d_f + w(v, u)
                    u.state_f = "OPEN"
                    u.pi_f = v
                    Q_f.insert(u)
                elif u.state_f == "OPEN":
                    if v.d_f + w(v, u) < u.d_f:
                        u.d_f = v.d_f + w(v, u)
                        u.pi_f = v
                        Q_f.update(u) 
                if (u.state_b == "OPEN" or u.state_b == "CLOSED"):
                    return (u.d_f + u.d_b, ExtractShortestPath(G, 1, u))
        else:
            v = Q_b.extractMin()
            v.state_b = "CLOSED"
            for u in sorted(G.predecessors(v), key=lambda node: node.id):
                if u.state_b == "UNVISITED":
                    u.d_b = v.d_b + w(u, v)
                    u.state_b = "OPEN"
                    u.pi_b = v
                    Q_b.insert(u)
                elif u.state_b == "OPEN":
                    if v.d_b + w(u, v) < u.d_b:
                        u.d_b = v.d_b + w(u, v)
                        u.pi_b = v
                        Q_b.update(u) 
                if (u.state_f == "OPEN" or u.state_f == "CLOSED"):
                    return (u.d_f + u.d_b, ExtractShortestPath(G, 1, u))
    return (math.inf, None) 

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
    mu = math.inf
    middle_vertex = None
    current_node_f = None
    current_node_b = None
    while (not Q_f.isEmpty()) and (not Q_b.isEmpty()):
        if (Q_f.min() <= Q_b.min()):
            v = Q_f.extractMin()
            current_node_f = v
            v.state_f = "CLOSED"
            if (current_node_b and current_node_f and current_node_f.d_f + current_node_b.d_b >= mu):
                return (mu, ExtractShortestPath(G, 1, middle_vertex))               
            for u in sorted(G.successors(v), key=lambda node: node.id):
                if u.state_f == "UNVISITED":
                    u.d_f = v.d_f + w(v, u)
                    u.state_f = "OPEN"
                    u.pi_f = v
                    Q_f.insert(u)
                elif u.state_f == "OPEN":
                    if v.d_f + w(v, u) < u.d_f:
                        u.d_f = v.d_f + w(v, u)
                        u.pi_f = v
                        Q_f.update(u) 
                if (u.state_b == "CLOSED" and v.d_f + u.d_b + w(v, u) < mu):
                    middle_vertex = v
                    mu = v.d_f + u.d_b + w(v, u)
        else:
            v = Q_b.extractMin()
            current_node_b = v
            v.state_b = "CLOSED"
            if (current_node_f.d_f + current_node_b.d_b > mu):
                return (mu, ExtractShortestPath(G, 1, middle_vertex)) 
            for u in sorted(G.predecessors(v), key=lambda node: node.id):
                if u.state_b == "UNVISITED":
                    u.d_b = v.d_b + w(u, v)
                    u.state_b = "OPEN"
                    u.pi_b = v
                    Q_b.insert(u)
                elif u.state_b == "OPEN":
                    if v.d_b + w(u, v) < u.d_b:
                        u.d_b = v.d_b + w(u, v)
                        u.pi_b = v
                        Q_b.update(u) 
                if (u.state_f == "CLOSED" and v.d_b + u.d_f + w(u, v) < mu):
                    middle_vertex = v
                    mu = v.d_b + u.d_f + w(u, v)
    if middle_vertex:
        return (mu, ExtractShortestPath(G, 1, middle_vertex)) 
    return (math.inf, None) 

def bidirectional_Dijkstra_10(G, w, s, t):
    """
    Search = after one edge \n
    End = same vertex close
    """
    def forward_one_edge(G, Q_f):
        while (not Q_f.isEmpty()):
            v = Q_f.extractMin()
            v.state_f = "CLOSED"
            if (v.state_b == "CLOSED"):
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
        return None
    
    def backward_one_edge(G, Q_b):
        while (not Q_b.isEmpty()):
            v = Q_b.extractMin()
            v.state_b = "CLOSED"
            if (v.state_f == "CLOSED"):
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
        return None

    init(G, s, t)
    Q_f = Queue()
    Q_f.insert(s)
    Q_b = Queue(False)
    Q_b.insert(t)
    fwd = True
    fwd_runner = forward_one_edge(G, Q_f)
    bwd_runner = backward_one_edge(G, Q_b)
    while (not Q_f.isEmpty()) and (not Q_b.isEmpty()):
        if (fwd):
            try:
                if(next(fwd_runner)):
                    u_min = FindMinDistVertex(G)
                    return (u_min.d_f + u_min.d_b, ExtractShortestPath(G, 1, u_min))
            except StopIteration:
                return (math.inf, None)
        else:
            try:
                if(next(bwd_runner)):
                    u_min = FindMinDistVertex(G)
                    return (u_min.d_f + u_min.d_b, ExtractShortestPath(G, 1, u_min))
            except StopIteration:
                return (math.inf, None)
        fwd = not fwd 
    for node in G.nodes():
        print(node.label + " " + node.state_f + " " + node.state_b)
    return (math.inf, None)

def bidirectional_Dijkstra_11(G, w, s, t):
    """
    Search = after one edge \n
    End = first encounter
    """
    def forward_one_edge(G, Q_f):
        while (not Q_f.isEmpty()):
            v = Q_f.extractMin()
            v.state_f = "CLOSED"            
            for u in sorted(G.successors(v), key=lambda node: node.id):
                if u.state_f == "UNVISITED":
                    u.d_f = v.d_f + w(v, u)
                    u.state_f = "OPEN"
                    u.pi_f = v
                    Q_f.insert(u)
                    yield (False, None)
                elif u.state_f == "OPEN":
                    if v.d_f + w(v, u) < u.d_f:
                        u.d_f = v.d_f + w(v, u)
                        u.pi_f = v
                        Q_f.update(u) 
                        yield (False, None)
                if (u.state_b == "OPEN" or u.state_b == "CLOSED"):
                    yield (True, u)
        return None
    
    def backward_one_edge(G, Q_b):
        while (not Q_b.isEmpty()):
            v = Q_b.extractMin()
            v.state_b = "CLOSED"
            for u in sorted(G.predecessors(v), key=lambda node: node.id):
                if u.state_b == "UNVISITED":
                    u.d_b = v.d_b + w(u, v)
                    u.state_b = "OPEN"
                    u.pi_b = v
                    Q_b.insert(u)
                    yield (False, None)
                elif u.state_b == "OPEN":
                    if v.d_b + w(u, v) < u.d_b:
                        u.d_b = v.d_b + w(u, v)
                        u.pi_b = v
                        Q_b.update(u) 
                        yield (False, None)
                if (u.state_f == "OPEN" or u.state_f == "CLOSED"):
                    yield (True, u)
        return None

    init(G, s, t)
    Q_f = Queue()
    Q_f.insert(s)
    Q_b = Queue(False)
    Q_b.insert(t)
    fwd = True
    fwd_runner = forward_one_edge(G, Q_f)
    bwd_runner = backward_one_edge(G, Q_b)
    while (not Q_f.isEmpty()) and (not Q_b.isEmpty()):
        if (fwd):
            try:
                end, encounter = next(fwd_runner)
                if(end): 
                    return (encounter.d_f + encounter.d_b, ExtractShortestPath(G, 1, encounter))
            except StopIteration:
                return (math.inf, None)
        else:
            try:
                end, encounter = next(bwd_runner)
                if(end): 
                    return (encounter.d_f + encounter.d_b, ExtractShortestPath(G, 1, encounter))
            except StopIteration:
                return (math.inf, None)
        fwd = not fwd
            
    return (math.inf, None)

def bidirectional_Dijkstra_12(G, w, s, t):
    """
    Search = after one edge \n
    End = using search distance
    """
    mu = math.inf
    middle_vertex = None
    current_node_f = None
    current_node_b = None

    def forward_one_edge(G, Q_f):
        nonlocal mu, middle_vertex, current_node_b, current_node_f
        while (not Q_f.isEmpty()):
            v = Q_f.extractMin()
            v.state_f = "CLOSED"
            current_node_f = v
            if (current_node_b and current_node_f and current_node_f.d_f + current_node_b.d_b > mu):
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
                if (u.state_b == "CLOSED" and v.d_f + u.d_b + w(v, u) < mu):
                    middle_vertex = v
                    mu = v.d_f + u.d_b + w(v, u)
        if middle_vertex:
            yield True
        return None
    
    def backward_one_edge(G, Q_b):
        nonlocal mu, middle_vertex, current_node_b, current_node_f
        while (not Q_b.isEmpty()):
            v = Q_b.extractMin()
            v.state_b = "CLOSED"
            current_node_b = v
            if (current_node_b and current_node_f and current_node_f.d_f + current_node_b.d_b > mu):
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
                if (u.state_f == "CLOSED" and v.d_b + u.d_f + w(u, v) < mu):
                    middle_vertex = v
                    mu = v.d_b + u.d_f + w(u, v)
        if middle_vertex:
            yield True
        return None

    init(G, s, t)
    Q_f = Queue()
    Q_f.insert(s)
    Q_b = Queue(False)
    Q_b.insert(t)
    fwd = True
    fwd_runner = forward_one_edge(G, Q_f)
    bwd_runner = backward_one_edge(G, Q_b)
    while (not Q_f.isEmpty()) and (not Q_b.isEmpty()):
        if (fwd):
            try:
                if(next(fwd_runner)):                   
                    return (mu, ExtractShortestPath(G, 1, middle_vertex))
            except StopIteration:
                return (math.inf, None)
        else:
            try:
                if(next(bwd_runner)):                   
                    return (mu, ExtractShortestPath(G, 1, middle_vertex))
            except StopIteration:
                return (math.inf, None)
        fwd = not fwd
            
    return (math.inf, None)
