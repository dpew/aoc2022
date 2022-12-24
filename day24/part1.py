#!/usr/bin/env python3

import sys
import os
import math
import pprint
from collections import defaultdict, deque
from queue import PriorityQueue
from typing import List, Dict, Any, Tuple

# create absolute mydir
mydir = os.path.abspath(os.path.dirname(__file__))
sys.path.append(os.path.join(mydir, '../lib'))

import advent

WINDS = {
        '>': (1, 0),
        '^': (0, -1),
        '<': (-1, 0),
        'v': (0, 1),
        }

MOVES = ((-1, 0), (1, 0), (0, -1), (0, 1), (0, 0))

class Wind:

    def __init__(self, pos, wind):
        self.pos = pos
        self.wind = wind
        self.direction = WINDS[wind]

    def next(self, gmin, gmax):
        bp = list(advent.addpos(self.pos, self.direction))
        if bp[0] >= gmax[0]:
            bp[0] = gmin[0] + 1
        elif bp[0] <= gmin[0]:
            bp[0] = gmax[0] - 1
        if bp[1] >= gmax[1]:
            bp[1] = gmin[1] + 1
        elif bp[1] <= gmin[1]:
            bp[1] = gmax[1] - 1
        self.pos = tuple(bp)

class Blizzard:

    def __init__(self):
        self.grid = defaultdict(lambda: '.')
        self.bliz = {}
        self.winds = []
        self.start = (1000, 1000)
        self.end = (-1, -1)
        self.min = (1000, 1000)
        self.max = (-1, -1)

    def add(self, pos, item):
        if item in WINDS.keys():
            self.bliz[pos] = item
            self.winds.append(Wind(pos, item))
            item = '.'
        self.grid[pos] = item
        if item == '.':
            if self.start[1] != min(self.start[1], pos[1]):
                self.start = pos
            if self.end[1] != max(self.end[1], pos[1]):
                self.end = pos
        self.max = advent.maxtuple(self.max, pos)
        self.min = advent.mintuple(self.min, pos)

    def next(self):
        newbliz = {}
        for w in self.winds:
            w.next(self.min, self.max)
            newbliz[w.pos] = w.wind
        self.bliz = newbliz

    def safe(self, pos):
        if pos == self.end:
            return True
        return pos[0] > self.min[0] and pos[0] < self.max[0] and \
               pos[1] > self.min[1] and pos[1] < self.max[1]

    def print(self, pos, mybliz=None):
        def thingat(tpos):
            if pos == tpos:
                return 'E'
            if mybliz:
                if pos in mybliz:
                   return mybliz[pos]
            else:
                if pos in self.bliz:
                   return self.bliz[pos]
            return self.grid[pos]

        s = ""
        for y in range(0, self.max[1]+1):
           s = s + (''.join(thingat((r,c)) for c in range(maxgrid[1]+1)))
        
class Node:
    def __init__(self, pos, time):
        self.pos = pos
        self.time = time
        self.eq = (pos, time)

    def __hash__(self):
        return hash(self.eq)

    def __eq__(self, other):
        return self.eq == other.eq

    def __repr__(self):
        return f"pos={self.pos} time={self.time}"

def main():
    try:
        input = sys.argv[1]
    except IndexError:
            input = "input.txt"
    with open(input) as f:
        data = list(r.rstrip() for r in f.readlines())

    blizzard = Blizzard()
    for y, row in enumerate(data):
        for x, item in enumerate(row):
            blizzard.add((x, y), item)

    global curtime
    curtime = 0
    # time: blizzard at time
    timedict = {}
    timedict[curtime] = blizzard.bliz

    def getBlizAtTime(t):
        global curtime
        while t > curtime:
            blizzard.next()
            curtime += 1
            timedict[curtime] = blizzard.bliz

        return timedict[t]

    start = Node(blizzard.start, 0)
    seen = set()
    Q = set()
    Q.add(start)

    def popmin():
        next = min(Q, key=lambda v: v.time)
        Q.remove(next)
        return next

    def neighbors(node: Node) -> Node:
        bliz = getBlizAtTime(node.time + 1)
        for d in MOVES:
            np = advent.addpos(node.pos, d)
            if blizzard.safe(np) and np not in bliz:
                yield Node(np, node.time+1)

    found = None
    while Q and not found:
        next = popmin()
        seen.add(next)
        print(f"STEP next={next}")
        for n in neighbors(next):
            if n.pos == blizzard.end:
                found = n
                break
            if n not in seen:
                Q.add(n)

    print(found)
    
if __name__ == '__main__':
    main()
