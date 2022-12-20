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
        self.external = False
        self.processed = False
        self.eq = (plane, start, direct)

    def __hash__(self):
        return hash(self.eq)

    def __eq__(self, other):
        return self.eq == other.eq

    def __repr__(self):
        return f"p={PLANES[self.plane]} s={self.start/2} d={self.direct}"

    def opposite(self):
        return Side(self.plane, self.start, -self.direct)

    def intersects(self, other):
        """
          True if the given side intersects this side 
        """
        print(f"intersects {self.plane} == {other.plane}")
        return self.plane != other.plane

class Cube(object):
    def __init__(self, pos: Tuple[int]):
        self.pos = pos
        self.gridpos = tuple(i * 2 for i in pos)
        sides = set()
        for plane in range(3):
            sides.add(Side(plane, self.gridpos[plane]-1, -1))
            sides.add(Side(plane, self.gridpos[plane]+1, 1))
        self.sides = sides
        self.external = False
        self.type = 'obsidian'

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

    # Find an initial exterior side
    minpos, maxpos = advent.minmax(*cubes.keys())    
    print((minpos, maxpos))

    filled = dict(cubes)

    def externalize(c: Cube):
        if c.type == 'fill':
            c.external = True
        for s in c.sides:
            s.external = True
            for adj in c.adjacent():
                if adj in filled:
                    nextcube = filled[adj]
                    for sadj in nextcube.sides:
                        if s.opposite() == sadj:
                            sadj.external = external
                    if nextcube.type == 'fill' and not nextcube.external:
                        externalize(nextcube)

    for x in range(minpos[0]-1, maxpos[0]+2):
        for y in range(minpos[1]-1, maxpos[1]+2):
            for z in range(minpos[2]-1, maxpos[2]+2):   
                pos = (x, y, z)
                if pos in filled:
                    continue
                c = Cube(pos)
                c.type = 'fill'
                filled[pos] = c
                # determine if external
                external = False
                if x < minpos[0] or x > maxpos[0] or y < minpos[1] or y > maxpos[1] or z < minpos[2] or z > maxpos[2]:
                    external = True
                else:
                    for adj in c.adjacent():
                        if adj in filled:
                            if filled[adj].external:
                                external = True
                c.external = external
                # print(f"{pos}: external={external}")
                if external:
                    externalize(c)
                    # for s in c.sides:
                    #     s.external = external
                    #     for adj in c.adjacent():
                    #         if adj in filled:
                    #             for sadj in filled[adj].sides:
                    #                 if s.opposite() == sadj:
                    #                     sadj.external = external

    # for c in cubes.values():
    #     for s in c.sides:
    #         if s.external and not s.processed:
    #             findexternal(c, s)

    uniqsides = {}
    for c in cubes.values():
        for s in c.sides:
            if s.external == True:
                uniqsides[id(s)] = s

    unprocessed = 0
    for c in cubes.values():
        for s in c.sides:
            if not s.processed:
                unprocessed += 1

    print(f"unprocessed: {unprocessed}")

    # print(uniqsides)
    print(len(uniqsides))


if __name__ == '__main__':
    main()