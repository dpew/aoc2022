#!/usr/bin/env python3

from __future__ import annotations

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

DIRECTIONS = {
    'N': ((0, -1), (-1, -1), (1, -1)),
    'S': ((0, 1), (-1, 1), (1, 1)),
    'W': ((-1, 0), (-1, -1), (-1, 1)),
    'E': ((1, 0), (1, -1), (1, 1))
}

LOOKAROUND = ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1))

ROUND_ROBIN = deque(['N', 'S', 'W', 'E'])

class Elves:
    def __init__(self):
        self.grove = defaultdict(lambda: '.')
        self.elves = set()

    def add(self, pos):
        self.grove[pos] = '#'
        self.elves.add(pos)

    def propose(self):
        self.proposed = {}
        self.count = defaultdict(int)
        # print(','.join(ROUND_ROBIN))
        for p, e in list(self.grove.items()):
            if e != '#':
                continue
            count = sum(self.grove[advent.addpos(p, la)] == '#' for la in LOOKAROUND)
            if count == 0:
                continue

            for d in ROUND_ROBIN:
                if p not in self.proposed:
                    count = sum(self.grove[advent.addpos(p, g)] == '#' for g in DIRECTIONS[d])
                    if count == 0:
                        nextpos = advent.addpos(p, DIRECTIONS[d][0])
                        self.proposed[p] = nextpos
                        self.count[nextpos] += 1
        ROUND_ROBIN.rotate(-1)

    def move(self) -> Elves:
        # print(self.proposed)
        # print(self.count)
        elves = Elves()
        for pos in self.elves:
            nx = None
            if pos in self.proposed:
                nx = self.proposed[pos]
                if self.count[nx] != 1:
                    nx = None
            if nx:
                elves.add(nx)
            else:
                elves.add(pos)
                
        return elves

    def emptycount(self):
        mn, mx = advent.minmax(*self.grove.keys())
        grovecount = (mx[1] - mn[1]) * (mx[0] - mn[0])
        return grovecount - len(self.elves)

    def print(self):        
        mn, mx = advent.minmax(*self.grove.keys())
        # print((mn, mx))
        for r in range(mn[1]-1, mx[1]+1):
            print(''.join(self.grove[(c, r)] for c in range(mn[0]-1, mx[0]+1)))

def main():
    try:
        input = sys.argv[1]
    except IndexError:
            input = "input.txt"
    with open(input) as f:
        data = list(r.rstrip() for r in f.readlines())

    elves = Elves()
    for r, row in enumerate(data):
        for c, elf in enumerate(row):
            if elf == '#':
                elves.add((c, r))


    elves.print()
    print(elves.emptycount())
    i = 0
    while True:
        i += 1
        elves.propose()
        if not elves.proposed:
            print(f"Went {i} rounds")
            break

        elves = elves.move()
        print(f"After round {i+1}")
        # elves.print()

if __name__ == '__main__':
    main()