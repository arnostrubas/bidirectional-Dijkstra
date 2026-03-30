# Copyright (c) 2026, Arnošt Rubáš
# All rights reserved.
# 
# This source code is licensed under the BSD 3-Clause License.
# The full text of the license can be found in the LICENSE file 
# in the root directory of this project.

import json

def graph_to_json(G):
    '''
    return JSON of given graph `G`
    '''
    nodes = []
    for node in G.nodes:
        label = str(node.id)
        if(node.id == -1):
            label = "START"
        elif (node.id == 0):
            label ="TARGET"
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
