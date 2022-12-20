#!/usr/bin/env python3

import sys
import os
import math
import pprint
from collections import defaultdict, deque
from queue import PriorityQueue
from typing import List, Dict, Any, Tuple, FrozenSet, Iterator, Generator
from sys import maxsize
from itertools import cycle

# create absolute mydir
mydir = os.path.abspath(os.path.dirname(__file__))
sys.path.append(os.path.join(mydir, '../lib'))

import advent


PLANES = {0: 'X',
          1: 'Y',
          2: 'Z'
          }

class Side(object):
    def __init__(self, plane: int, start: int, direct: int):
        '''
           plane: 0=x, 1=y, 2=z
           start: beginning of the plane
           direction: -1 or 1
        '''
        self.plane = plane
        self.start = start
        self.direct = direct
        self.eq = (plane, start, direct)

    def __hash__(self):
        return hash(self.eq)

    def __eq__(self, other):
        return self.eq == other.eq

    def __repr__(self):
        return f"p={PLANES[self.plane]} s={self.start} d={self.direct}"

    def opposite(self):
        return Side(self.plane, self.start, -self.direct)

class Cube(object):
    def __init__(self, pos: Tuple[int]):
        self.pos = pos
        self.gridpos = tuple(i * 2 for i in pos)
        sides = set()
        for plane in range(3):
            sides.add(Side(plane, self.gridpos[plane]-1, -1))
            sides.add(Side(plane, self.gridpos[plane]+1, 1))
        self.sides = sides

    def adjacent(self):
        '''
        Returns cube positions adjacent to this cube
        '''
        for plane in range(3):
            p = list(self.pos)
            p[plane] -= 1
            yield tuple(p)
            p[plane] += 2
            yield tuple(p)

    def mergeside(self, side):
        '''
           Remove our side and use that other side
        '''
        # Remove same side
        self.sides.remove(side)
        # Add this instance
        self.sides.add(side)

    def rmside(self, side):
        '''
            Remove side, like if it opposes other side
        '''
        self.sides.remove(side)

    def __repr__(self):
        return repr(self.pos)

def main():
    try:
        input = sys.argv[1]
    except IndexError:
            input = "input.txt"
    with open(input) as f:
        data = list(r.rstrip() for r in f.readlines())


    cubes: Dict[Tuple[int], Cube] = {}
    for row in data:
        pos = tuple(int(x) for x in row.split(","))
        cubes[pos] = Cube(pos)

    print(cubes)
    # Remove adjacent sides
    for c in cubes.values():
        sides = set(c.sides)
        for ap in c.adjacent():
            if ap not in cubes:
                continue
            adj = cubes[ap]
            for sadj in set(adj.sides):
                oadj = sadj.opposite()
                if oadj in sides:
                    c.rmside(oadj)
                    adj.rmside(sadj)

    uniqsides = {}
    for c in cubes.values():
        for s in c.sides:
            uniqsides[id(s)] = s

    # print(uniqsides)
    print(len(uniqsides))

    # Merge sides
    for c in cubes.values():
        sides = set(c.sides)
        for ap in c.adjacent():
            if ap not in cubes:
                continue
            adj = cubes[ap]
            for sadj in set(adj.sides):
                if sadj in sides:
                    # print(sadj)
                    # print(adj.sides)
                    # print(sides)
                    c.mergeside(sadj)

    uniqsides = {}
    for c in cubes.values():
        for s in c.sides:
            uniqsides[id(s)] = s

    # print(uniqsides)
    print(len(uniqsides))


if __name__ == '__main__':
    main()