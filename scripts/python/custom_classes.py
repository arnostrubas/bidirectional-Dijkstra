# Copyright (c) 2026, Arnošt Rubáš
# All rights reserved.
# 
# This source code is licensed under the BSD 3-Clause License.
# The full text of the license can be found in the LICENSE file 
# in the root directory of this project.

import networkx as nx # type: ignore
import heapq

class Node:
    '''
    Custom class representing node of the graph.
    '''
    def __init__(self, id, label, d_f = None, pi_f = None, state_f = None, d_b = None, pi_b = None, state_b = None):
        self.id = id
        self.label = label
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
    def __init__(self, text="", queue_f = Queue(), queue_b = Queue()):
        self.queue_f = queue_f
        self.queue_b = queue_b
        self.text = text