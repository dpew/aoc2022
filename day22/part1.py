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

TURN = {
    'R': 90,
    'L': -90 
}

DVALUE = {
    (1, 0): 0,
    (0, 1): 1,
    (-1, 0): 2,
    (0, -1): 3
}

import advent

class Grove(object):

    def __init__(self):
        self.grid = defaultdict(lambda: ' ')
        self.start = None
        self.pos = None
        self.height = 0
        self.width = 0
        self.direction = (1, 0)

    def add_row(self, row: Iterator[str]):
        for x, d in enumerate(row):
            self.grid[(x, self.height)] = d
            if self.start is None and d == '.':
                self.start = (x, self.height)
                self.pos = self.start
        self.height += 1
        self.width = max(self.width, len(row))

    def step(self):
        nextpos = ((self.pos[0] + self.direction[0]) % self.width, (self.pos[1] + self.direction[1]) % self.height)
        while self.grid[nextpos] == ' ':
            nextpos = ((nextpos[0] + self.direction[0]) % self.width, (nextpos[1] + self.direction[1]) % self.height)

        # Stop
        if self.grid[nextpos] == '#':
            return

        self.pos = nextpos

    def move(self, steps: Any):
        if steps in ('L', 'R'):
            self.turn(steps)
        else:
            for m in range(steps):
                self.step()

    def turn(self, direct: str):
        if direct == 'R':
            direction = advent.rotate2(self.direction, 90)
        elif direct == 'L':
            direction = advent.rotate2(self.direction, -90)
        else:
            raise ValueError(dir)
        self.direction = direction

    @property
    def mypos(self):
        return advent.subpos(self.pos, self.start)
        
def process_moves(moves: str):
    buffer = ''
    for c in moves:
        if c in ('L', 'R'):
            if buffer:
                yield int(buffer)
                buffer = ''
            yield c
        else:
            buffer = buffer + c
    if buffer:
        yield int(buffer)



def main():
    try:
        input = sys.argv[1]
    except IndexError:
            input = "input.txt"
    with open(input) as f:
        data = list(r.rstrip() for r in f.readlines())

    grove = Grove()
    gmoves = False
    for row in data:
        if row.strip():
            if gmoves:
                moves = row
            else:                
                grove.add_row(row)
        else:
            gmoves = True

    assert grove.mypos == (0, 0)
    for m in process_moves(moves):
        print(m)
        grove.move(m)
        print(f"pos={grove.pos}, rpos={grove.mypos} dir={grove.direction}")


    pos = grove.pos
    value = 1000 * (pos[1]+1) + 4 * (pos[0]+1) + DVALUE[grove.direction]
    print(value) 



if __name__ == '__main__':
    main()