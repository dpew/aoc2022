#!/usr/bin/env python3

import sys
import os
import math
import pprint
from collections import defaultdict, deque
from queue import PriorityQueue
from typing import List, Dict, Any, Tuple, FrozenSet
from sys import maxsize
from itertools import chain

# create absolute mydir
mydir = os.path.abspath(os.path.dirname(__file__))
sys.path.append(os.path.join(mydir, '../lib'))

import advent

class Node(object):
    def __init__(self, name: str, flow: int):
        self.name = name
        self.flow = flow
        self.vert = []

    def __repr__(self):
        return f"Valve {self.name} has flow rate={self.flow}; tunnels lead to valves {self.vert}"

def parse(data: List[str]) -> Dict[str, Node]:
    nodes = {}
    verticies = {}
    for line in data:
        l = list(advent.tokenize(line, ' =;,'))
        node = Node(l[1], int(l[5]))
        for v in l[10:]:
            node.vert.append(v)
        nodes[node.name] = node

    return nodes

class Path(object):
    def __init__(self, node: str, time: int, opened: FrozenSet[str], value: int):
        self.node = node
        self.time = time
        self.opened = opened
        self.value = value
        self.eq = (self.node, self.time, self.opened, self.value)

    def __hash__(self):
        return hash(self.eq)

    def __eq__(self, other):
        return self.eq == other.eq

    def __repr__(self):
        return f"node={self.node} val={self.value} t={self.time} opened={self.opened}"

def main():
    try:
        input = sys.argv[1]
    except IndexError:
            input = "input.txt"
    with open(input) as f:
        data = list(r.rstrip() for r in f.readlines())

    nodes = parse(data)
    print("\n".join(repr(n) for n in nodes.values()))

    pos = Path('AA', 30, frozenset(), 0)
    seen = set()
    Q = set()    
    Q.add(pos)

    def findmax():
        # print(f"POPMIN Q={Q}")
        next = max(Q, key=lambda v: (v.time, v.value))
        Q.remove(next)
        # print(f"POPMIN {next} {Q}")
        return next


    def neighbors(pos: Path):
        # if value has not been opened, open it
        node = nodes[pos.node]
        time = pos.time - 1
        if time == 0:
            return

        if pos.node not in pos.opened:
            yield Path(pos.node, time, frozenset(chain(pos.opened, [pos.node])), pos.value + node.flow * pos.time)

        for n in node.vert:
            if n in pos.opened:
                continue
            yield Path(n, time, pos.opened, pos.value)

        
    
    while Q:
        next = findmax()
        seen.add(next)
        # print(f"STEP next={next}")
        for n in neighbors(next):
            if n.time == 1:
                print(n)
                sys.exit(0)
            # print(repr(n))
            Q.add(n)

if __name__ == '__main__':
    main()