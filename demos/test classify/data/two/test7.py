# -*- coding: utf-8 -*-
#/usr/bin/python

from collections import deque
import sys

class Graph(object):
    def __init__(self, *args, **kwargs):
        self.order = []     #visited order
        self.neighbor = {}
    
    def add_node(self, node):
        key,val = node
        if not isinstance(val, list):
            print('node value should be a list')
        #sys.exit('failed for wrong input')
        
        self.neighbor[key] = val
    
    def broadth_first(self, root):
        if root != None:
            search_queue = deque()
            search_queue.append(root)
            
            visited = []
        else:
            print('root is None')
            return -1
        
        while search_queue:
            person = search_queue.popleft()
            self.order.append(person)
            
            if (not person in visited) and (person in self.neighbor.keys()):
                search_queue += self.neighbor[person]
                visited.append(person)


def depth_first(self, root):
    if root != None:
        search_queue = deque()
        search_queue.append(root)
        
            visited = []
        else:
            print('root is None')
            return -1
    
        while search_queue:
            person = search_queue.popleft()
            self.order.append(person)
            
            if (not person in visited) and (person in self.neighbor.keys()):
                tmp = self.neighbor[person]
                tmp.reverse()
                
                for index in tmp:
                    search_queue.appendleft(index)
                
                visited.append(person)
                    #self.order.append(person)
                    
                    
                    def clear(self):
                        self.order = []
                            
                            def node_print(self):
                                for index in self.order:
                                    print(index, end='  ')


if __name__ == '__main__':
    g = Graph()
    g.add_node(('1',['one', 'two','three']))
    g.add_node(('one',['first','second','third']))
    g.add_node(('two',['1','2','3']))
    
    g.broadth_first('1')
    
    print('broadth search first:')
    print('  ', end='  ')
    g.node_print()
    
    g.clear()
    
    print('\n\ndepth search first:')
    print('  ', end='  ')
    g.depth_first('1')
    
    g.node_print()
    print()
