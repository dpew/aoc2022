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
    def __init__(self, node: str, time: int, opened: FrozenSet[str], value: int = 0, flow: int = 0):
        self.node = node
        self.time = time
        self.opened = opened
        self.value = value
        self.flow = flow
        self.eq = (self.node, self.opened, self.value, self.time)

    def __hash__(self):
        return hash(self.eq)

    def __eq__(self, other):
        return self.eq == other.eq

    def goTo(self, newnode: str):
        return Path(newnode, self.time + 1, self.opened, self.flow + self.value, self.flow)

    def openValve(self, flow: int):
        newflow = self.flow + flow
        opened = tuple(chain(self.opened, [self.node]))
        return Path(self.node, self.time + 1, opened=opened, value=(self.flow + self.value), flow=newflow)


    def __repr__(self):
        return f"node={self.node} t={self.time} v={self.value} f={self.flow} opened={self.opened}"

def main():
    try:
        input = sys.argv[1]
    except IndexError:
            input = "input.txt"
    with open(input) as f:
        data = list(r.rstrip() for r in f.readlines())

    nodes = parse(data)
    print("\n".join(repr(n) for n in nodes.values()))

    seen = set()
    pos = Path('AA', 0, frozenset(), 0)
    
    def findmax():
        # print(f"POPMIN Q={Q}")
        next = max(Q, key=lambda v: v.value)
        Q.remove(next)
        # print(f"POPMIN {next} {Q}")
        return next

    def neighbors(pos: Path):
        # if value has not been opened, open it
        node = nodes[pos.node]

        # open flow
        if pos.node not in pos.opened and node.flow > 0:
            yield pos.openValve(node.flow)

        for n in node.vert:
            yield pos.goTo(n)


    path31 = deque()
    def dfs(p: Path):
        for n in neighbors(p):
            if n in seen:
                continue
            if n.time == 30:
                path31.append(n)
                return
            seen.add(n)
            dfs(n)

    dfs(pos)
    mval = max(path31, key=lambda x: x.value)

    print("ANSWER")
    print(mval)
    #print(f"max = {mval.value}")
    # print(seen)

if __name__ == '__main__':
    main()