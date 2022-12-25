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

SIDES = {
          'X0': (0, None, None),
          'X1': (1, None, None),
          'Y0': (None, 0, None),
          'Y1': (None, 1, None),
          'Z0': (None, None, 0),
          'Z1': (None, None, 1)
        }

class Side:

    def __init__(self, side: Tuple[int]):
        self.side = side
        self.grid = {}
        assert len(side) == 3
        assert sum(i is not None for i in side) == 1

    def put(self, pos, val):
        if pos in self.grid:
            raise KeyError(f"Side: {self.side} pos={pos}")
        self.grid[pos] = val

    def __getitem__(self, pos):
        return self.grid[pos]


def rotateX(direc, deg):
    vec = advent.pos_to_vector3(direc)
    mul = advent.rotateX(deg)
    return advent.vector3_to_pos(np.dot(vec, mul))

def rotateY(direc, deg):
    vec = advent.pos_to_vector3(direc)
    mul = advent.rotateY(deg)
    return advent.vector3_to_pos(np.dot(vec, mul))


def rotateZ(direc, deg):
    vec = advent.pos_to_vector3(direc)
    mul = advent.rotateZ(deg)
    return advent.vector3_to_pos(np.dot(vec, mul))

def turn(side, vector, direct):
        deg = 0
        if direct == 'R':
            deg = 90
        elif direct == 'L':
            deg = -90
        else:
            raise ValueError("BAD direction " + direct)

        if side == (None, None, 1):
            direction = rotateZ(vector, -deg)
        elif side == (None, None, 0):
            direction = rotateZ(vector, deg)
        elif side == (None, 1, None):
            direction = rotateY(vector, -deg)
        elif side == (None, 0, None):
            direction = rotateY(vector, deg)
        elif side == (1, None, None):
            direction = rotateX(vector, -deg)
        elif side == (0, None, None):
            direction = rotateX(vector, deg)
        else:
            raise ValueError("BAD side " + side)
        return direction


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
        ((0, 0, 3), (0, None, None))
        >>> translate_3d((-3, 7), 4)
        ((0, 2, 3), (0, None, None))
    '''
    print(f't3d {pos}')
    sideX = math.floor(pos[0] / size)
    sideY = math.floor(pos[1] / size)
    posX = pos[0] % size
    nposY = pos[1] % size
    nposX = size - posX - 1
    posY = size - nposY - 1
    
    if sideY == 0:
        if sideX == 0:
            return ((posX, posY, 0), SIDES['Z0'])
        if sideX == 1:
            return ((1, posY, posX), SIDES['X1'])
    if sideY == 1:
        if sideX == 0:
            return ((posX, 0, nposY), SIDES['Y0'])
        if sideX == -1:
            return ((0, nposX, nposY), SIDES['X0'])
        if sideX == -2:
            return ((nposX, 1, nposY), SIDES['Y1'])
    if sideY == 2:
        if sideX == 0:
            return ((posX, nposY, 1), SIDES['Z1'])
        if sideX == -1:
            return ((0, nposY, posX), SIDES['X0'])
        if sideX == -2:
            return ((0, nposY, posX), SIDES['X0'])
    if sideY == 2:
        if sideX == 0:
            return ((posX, nposY, 1), SIDES['Z1'])
        if sideX == -1:
            return ((0, nposY, posX), SIDES['X0'])
        if sideX == 1:
            return ((1, nposY, nposX), SIDES['X1'])
    raise ValueError((sideX, sideY))

class Grove(object):

    def __init__(self, cubewidth: int):
        self.grid = {}
        for side in SIDES.values():
            self.grid[side] = Side(side)
        self.height = 0
        self.start = None
        self.pos = (0, 0, 0)
        self.direction = (1, 0, 0)
        self.cubewidth = cubewidth
        self.curside = SIDES['Z0']

    def print(self):
        for sname, sval in SIDES.items():
            print(f"SIDE {sname}:")
            side = self.grid[sval]
            for y in range(self.cubewidth):
                print(''.join(side[(x, y)] for x in range(self.cubewidth)))
            print()

    def add_row(self, row: Iterator[str]):
        for x, d in enumerate(row):
            mypos = (x, self.height)
            if self.start is None and d == '.':
                self.start = mypos
            if self.start and d != ' ':
                relpos = advent.subpos(mypos, self.start)
                p3, sd = translate_3d(relpos, self.cubewidth)
                self.grid[sd].put(p3, d)

        self.height += 1

    def step(self):
        def fdirect(x):
            if x is None:
                return 0
            if x == 0:
                return 1
            return -1
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
        for d in (0, 1, 2):
            if nextpos[d] >= self.cubewidth or nextpos[d] < 0:
                nval = 1 if nextpos[d] < 0 else 0
                nextdir = tuple(fdirect(c) for c in self.curside)
                nextside = tuple(nval if i == d else None for i in range(3))
                nextpos = tuple(fnextpos(c, d, nval) for c in range(3))
                print(f" curside={self.curside} direction={self.direction} pos={self.pos}")
                print(f"nextside={nextside} nextdir={nextdir} nextpos={nextpos}")

        # If next position is not a wall
        pprint.pprint(self.grid[nextside].grid)
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
        newdirect = turn(self.curside, self.direction, direct)
        self.direction = newdirect

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
    #grove.print()

    for m in process_moves(moves):
        print(m)
        grove.move(m)
        print(f"pos={grove.pos}, dir={grove.direction}")


    pos = grove.pos
    value = 1000 * (pos[1]+1) + 4 * (pos[0]+1) + DVALUE[grove.direction]
    print(value) 



if __name__ == '__main__':
    import doctest
    doctest.testmod()
    main()
