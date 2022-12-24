#!/usr/bin/env python3

import sys
import os
import math
import pprint
from collections import defaultdict, deque
from queue import PriorityQueue
from typing import List, Dict, Any, Tuple, FrozenSet, Iterator, Generator
import numpy as np

# create absolute mydir
mydir = os.path.abspath(os.path.dirname(__file__))
sys.path.append(os.path.join(mydir, '../lib'))

import advent

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

SIDES = ((0, None, None), (1, None, None),
         (None, 0, None), (None, 1, None),
         (None, None, 0), (None, None, 1))


class Side:

    def __init__(self, side: Tuple[int]):
        self.side = side
        self.grid = {}
        assert len(side) == 3
        assert sum(i is not None for i in side) == 1

    def put(self, pos, val):
        self.grid[pos] = val

    

def translate_3d(pos: Tuple[int], size: int) -> Tuple[int]:
    '''
        Translates from 2d to 3d using the folding
        >>> translate_3d((0, 0), 4)
        ((0, 3, 0), (None, None, 0))
        >>> translate_3d((1, 3), 4)
        ((1, 0, 0), (None, None, 0))
        >>> translate_3d((2, 4), 4)
        ((2, 0, 0), (None, 0, None))
        >>> translate_3d((3, 7), 4)
        ((3, 0, 3), (None, 0, None))
        >>> translate_3d((-1, 7), 4)
        ((0, 3, 3), (0, None, None))
        >>> translate_3d((-3, 7), 4)
        ((0, 1, 3), (0, None, None))
    '''
    sideX = math.floor(pos[0] / size) % 2
    sideY = math.floor(pos[1] / size)
    posX = pos[0] % size
    posY = pos[1] % size
    return ((posX, posY), (sideX, sideY))

class Grove(object):

    def __init__(self, cubewidth: int):
        self.grid = {}
        for side in SIDES:
            self.grid[side] = Side(side)
        self.start = None
        self.pos = None
        self.direction = (1, 0)
        self.cubewidth = cubewidth


    def add_row(self, row: Iterator[str]):
        for x, d in enumerate(row):
            mypos = (x, self.height)
            if self.start is None and d == '.':
                self.start = mypos
                self.pos = self.start
            if self.start:
                relpos = advent.subpos(mypos, self.start)
                p3, sd = translate_3d(relpos)
                self.grid[sd].put(p3, d)

        self.height += 1

    def step(self):
        def fdirect(x):
            if x is None:
                return 0
            if x == 0:
                return 1
            if return -1
        def fnextpos(dimen, flopside, newflop):
            # dimension if the new side (flopside), so return the new flop value
            if dimen == flopside:
                return newflop
            # dimension is the previous side, so use the cubewidth or 0
            if self.curside[dimen] == 1:
                return self.cubewidth-1
            if self.curside[dimen] == 0:
                return 0
            # Return the old dimension position
            return self.pos[dimen]


        nextpos = advent.addpos(self.pos, self.direction)
        nextdir = self.direction
        nextside = self.curside
        for d in dimension:
            if nextpos[d] >= self.cubewidth or nextpos[d] < 0:
                nval = 0 if nextpos[d] < 0 else 1
                nextdir = tuple(fdirect(c) for c in self.curside)
                nextpos = tuple(fnextpos(c, d, nval) for c in range(3))
                nextside = tuple(1 if i == d else None in i range(3))

        # If next position is not a wall
        if self.grid[nextside][nextpos] != '#':
            self.curside = nextside
            self.direction = nextdir
            self.pos = nextpos
            
    def move(self, steps: Any):
        if steps in ('L', 'R'):
            self.turn(steps)
        else:
            for m in range(steps):
                self.step()

    def turn(self, direct: str):
        deg = 0
        if direct == 'R':
            deg = 90
        elif direct == 'L':
            deg = -90
        else:
            raise ValueError("BAD direction " + direct)

        if self.curside == (None, None, 1):
            direction = rotateZ(self.direction, deg)
        elif self.curside == (None, None, 0):
            direction = rotateZ(self.direction, -deg)
        elif self.curside == (None, 1, None):
            direction = rotateY(self.direction, deg)
        elif self.curside == (None, 0, None):
            direction = rotateY(self.direction, -deg)
        elif self.curside == (1, None, None):
            direction = rotateX(self.direction, deg)
        elif self.curside == (0, None, None):
            direction = rotateX(self.direction, -deg)
        else
            raise ValueError("BAD side " + self.curside)
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
    if len(data) < 16:
        cwidth = 4
    else:
        cwidth = 50

    grove = Grove(cwidth)
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
    import doctest
    doctest.testmod()
    main()
