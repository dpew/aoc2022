#!/usr/bin/env python3

import sys
import os
import math
import pprint
from collections import defaultdict, deque
from queue import PriorityQueue
from typing import List, Dict, Any, Tuple, FrozenSet, Iterator, Generator
import numpy as np

mydir = os.path.abspath(os.path.dirname(__file__))
sys.path.append(os.path.join(mydir, '../lib'))

import advent

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


SIDES = {
          'X0': (0, None, None),
          'X1': (1, None, None),
          'Y0': (None, 0, None),
          'Y1': (None, 1, None),
          'Z0': (None, None, 0),
          'Z1': (None, None, 1)
        }

def doturn(sname, vector, direct):
    side = SIDES[sname]
    nvector = turn(side, vector, direct)
    print(f"side={sname}[{direct}] {vector} -> {nvector}")
    return nvector

for s in 'X0', 'X1':
    for d in 'R', 'L':
        start = (0, 1, 0)
        for i in range(4):
            start = doturn(s, start, d) 

for s in 'Y0', 'Y1':
    for d in 'R', 'L':
        start = (1, 0, 0)
        for i in range(4):
            start = doturn(s, start, d) 

for s in 'Z0', 'Z1':
    for d in 'R', 'L':
        start = (1, 0, 0)
        for i in range(4):
            start = doturn(s, start, d) 
