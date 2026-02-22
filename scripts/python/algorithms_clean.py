#region Just to avoid compiler errors
def Queue():
    pass
def init():
    pass
def NCPP():
    pass
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
    fwd = True                     # for visualisation purposes
    while (not Q_f.isEmpty()) and (not Q_b.isEmpty()):
        if (fwd):
            v = Q_f.extractMin()
            v.state_f = "CLOSED"
            if (v.state_b == "CLOSED"):
                min = NCPP(G, 1)
                return min                
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
                min = NCPP(G, 1)
                return min  
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
                    return NCPP(G, 1)
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
                    return NCPP(G, 1)
            fwd = not fwd
    return 

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
    while (not Q_f.isEmpty()) and (not Q_b.isEmpty()):
        if (fwd):
            v = Q_f.extractMin()
            current_node_f = v
            v.state_f = "CLOSED"
            if (current_node_b and current_node_f and current_node_f.d_f + current_node_b.d_b >= mu):
                return NCPP(G, 2, middle_vertex)         
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
                return NCPP(G, 2, middle_vertex)           
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
    return 

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
    while (not Q_f.isEmpty()) and (not Q_b.isEmpty()):
        if (Q_f.count <= Q_b.count):
            v = Q_f.extractMin()
            v.state_f = "CLOSED"
            if (v.state_b == "CLOSED"):
                return NCPP(G, 1)                
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
                return NCPP(G, 1) 
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
    while (not Q_f.isEmpty()) and (not Q_b.isEmpty()):
        if (Q_f.count <= Q_b.count):
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
                    return NCPP(G, 1)
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
                    return NCPP(G, 1)
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
    while (not Q_f.isEmpty()) and (not Q_b.isEmpty()):
        if (Q_f.count <= Q_b.count):
            v = Q_f.extractMin()
            current_node_f = v
            v.state_f = "CLOSED"
            if (current_node_b and current_node_f and current_node_f.d_f + current_node_b.d_b >= mu):
                return NCPP(G, 2, middle_vertex)             
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
                return NCPP(G, 2, middle_vertex)
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
    while (not Q_f.isEmpty()) and (not Q_b.isEmpty()):
        if (Q_f.min() <= Q_b.min()):
            v = Q_f.extractMin()
            v.state_f = "CLOSED"
            if (v.state_b == "CLOSED"):
                return NCPP(G, 1)                 
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
                return NCPP(G, 1)  
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
                    return NCPP(G, 1)
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
                    return NCPP(G, 1)
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
    while (not Q_f.isEmpty()) and (not Q_b.isEmpty()):
        if (Q_f.min() <= Q_b.min()):
            v = Q_f.extractMin()
            current_node_f = v
            v.state_f = "CLOSED"
            if (current_node_b and current_node_f and current_node_f.d_f + current_node_b.d_b >= mu):
                return NCPP(G, 2, middle_vertex)              
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
                return NCPP(G, 2, middle_vertex)
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
            yield False
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
                    return NCPP(G, 1)
            except StopIteration:
                return None
        else:
            try:
                if(next(bwd_runner)):
                    return NCPP(G, 1)
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
                    yield True
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
                    yield False
                elif u.state_b == "OPEN":
                    if v.d_b + w(u, v) < u.d_b:
                        u.d_b = v.d_b + w(u, v)
                        u.pi_b = v
                        Q_b.update(u) 
                        yield False
                if (u.state_f == "OPEN" or u.state_f == "CLOSED"):
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
                    return NCPP(G, 1)
            except StopIteration:
                return None
        else:
            try:
                if(next(bwd_runner)): 
                    return NCPP(G, 1)
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
        return None
    
    def backward_one_edge(G, Q_b):
        nonlocal mu, middle_vertex, current_node_b, current_node_f
        while (not Q_b.isEmpty()):
            v = Q_b.extractMin()
            v.state_b = "CLOSED"
            current_node_b = v
            yield False
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
                    return NCPP(G, 2, middle_vertex)
            except StopIteration:
                return None
        else:
            try:
                if(next(bwd_runner)):                   
                    return NCPP(G, 2, middle_vertex)
            except StopIteration:
                return None
        fwd = not fwd
            
    return None
