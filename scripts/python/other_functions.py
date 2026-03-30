# Copyright (c) 2026, Arnošt Rubáš
# All rights reserved.
# 
# This source code is licensed under the BSD 3-Clause License.
# The full text of the license can be found in the LICENSE file 
# in the root directory of this project.

import networkx as nx # type: ignore

def node_from_graph(G, id):
    '''
    returns node with `id` in graph `G`, otherwise None
    '''
    index = G.graph.get('nodes_by_id', {})
    return index.get(id)

def node_on_path(node):
    '''
    Changes states of `node` so it is highlighted in graph visualisation
    '''
    node.state_f = "PATH"
    node.state_b = "PATH"

def edge_on_path(G, id1, id2):
    '''
    changes state of edge between `id1` and `id2` so that it is highlighted in graph visualisation
    '''
    G[node_from_graph(G, id1)][node_from_graph(G, id2)]['state'] = "PATH"

