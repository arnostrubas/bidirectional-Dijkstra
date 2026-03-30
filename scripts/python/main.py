# Copyright (c) 2026, Arnošt Rubáš
# All rights reserved.
# 
# This source code is licensed under the BSD 3-Clause License.
# The full text of the license can be found in the LICENSE file 
# in the root directory of this project.

import networkx as nx # type: ignore
from functools import partial
from js import window # type: ignore
import json
from other_functions import *
from algorithms import *
from json_functions import *

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
            "text": yielded.text
        } 
        result.append(json.dumps(data))
    res =  {
        "data": result,
    }
    return json.dumps(res)

def run_algorithm(graph_dict):
    '''
    runs algorithm with parameters specified in graph_dict
    '''
    search = graph_dict["search"]
    end = graph_dict["end"]
    graph_dict = graph_dict["graph"]
    nodes = graph_dict["nodes"]
    edges = graph_dict["edges"]

    G = nx.DiGraph()
    nodes_by_id = {}
    for node in nodes:
        n = Node(int(node["id"]), node["label"])
        G.add_node(n)
        nodes_by_id[n.id] = n
    G.graph['nodes_by_id'] = nodes_by_id
    for edge in edges:
        u_id = edge["source"]
        v_id = edge["target"]
        u = node_from_graph(G, int(u_id))
        v = node_from_graph(G, int(v_id))
        weight = edge["weight"]
        G.add_edges_from([(u, v, {'weight': int(weight), 'state': 'EMPTY', 'id': edge["id"]})])
    
    return visualise_algorithm(G, search, end)
    
def run(JSON):
    '''
    runs algorithms with parameters specified in JSON
    '''
    json_dict = json.loads(JSON)
    part_one = json_dict["part_one"]
    part_two = json_dict["part_two"]
    result = {
        "part_one": {
            "steps": run_algorithm(part_one),
        },
        "part_two": {
            "steps": run_algorithm(part_two),
        }
    }
    return json.dumps(result)
#endregion

#allows run to be accessed from JavaScript
window.run = run

window.python_ready()