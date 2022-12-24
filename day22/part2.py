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




def translate_3d(pos: Tuple[int], size: int) -> Tuple[int]:
    '''
        Translates from 2d to 3d using the folding
    '''
    foldsX = int(pos[0] / size)
    foldsY = int(pos[1] / size)

     matrix = advent.translate(0, 0, 0)
    for i in range(foldsY):
        matrix = np.dot(advent.translate(0, -size*foldsY, 0))
        matrix = np.dot(matrix, advent.rotateX(-90))

    if foldsX == 0:
        pass
    elif foldsX == -1:
        matrix = np.dot(advent.translate(-size*foldsX, 0, 0))
        matrix = np.dot(matrix, advent.rotateY(90))
    elif foldsX > 1:
        matrix = np.dot(advent.translate(-size*foldsX, 0, 0))
        matrix = np.dot(matrix, advent.rotateY(-90))

    pos2d = (pos[0], [pos[1]], 0, 1)
    pos3d = np.dot(pos2d, matrix)
    return tuple(pos3d[:3])

class Grove(object):

    def __init__(self, cubewidth: int):
        self.grid = defaultdict(lambda: ' ')
        self.grid3 = defaultdict(lambda: ' ')
        self.start = None
        self.pos = None
        self.height = 0
        self.width = 0
        self.direction = (1, 0)
        self.cubewidth = cubewidth

    def threeD(self, pos2: Tuple[int]):
        pos2 = tuple(x % (self.cubewidth * 4) for x in pos2)
        y = 0
        if pos2[0] >= 0 and pos2[0] < self.cubewidth:
            x = pos2[0]
            z = 0
        elif pos2[0] >= self.cubewidth and pos2[0] < self.cubewidth*2:
            x = self.cubewidth
            z = pos2[0]
        elif pos2[0] >= self.cubewidth*2 and pos2[0] < self.cubewidth*3:
            x = self.cubewidth - pos2[0]
            z = self.cubewidth
        elif pos2[0] >= self.cubewidth*3 and pos2[0] < self.cubewidth*4:
            x = 0
            z = self.cubewidth - pos2[0]

        if pos2[1] >= 0 and pos2[1] < self.cubewidth:
            y = pos2[0]
            z = 0
        elif pos2[1] >= self.cubewidth and pos2[1] < self.cubewidth*2:
            x = self.cubewidth
            y = pos2[0]
        elif pos2[1] >= self.cubewidth*2 and pos2[1] < self.cubewidth*3:
            x = self.cubewidth - pos2[0]
            y = self.cubewidth
        elif pos2[1] >= self.cubewidth*3 and pos2[1] < self.cubewidth*4:
            x = 0
            y = self.cubewidth - pos2[0]

        return (x, y, z)



    def add_row(self, row: Iterator[str]):
        for x, d in enumerate(row):
            mypos = (x, self.height)
            self.grid[mypos] = d
            if self.start is None and d == '.':
                self.start = mypos
                self.pos = self.start
            if d != ' ':
                relpos = advent.subpos(mypos, self.start)
                pos3d = self.threeD(relpos)
                print(f"pod={mypos} relpos={relpos} 3d={pos3d}")

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
    main()