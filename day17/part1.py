#!/usr/bin/env python3

import sys
import os
import math
import pprint
from collections import defaultdict, deque
from queue import PriorityQueue
from typing import List, Dict, Any, Tuple, FrozenSet, Iterator
from sys import maxsize
from itertools import chain

# create absolute mydir
mydir = os.path.abspath(os.path.dirname(__file__))
sys.path.append(os.path.join(mydir, '../lib'))

import advent

class Rock(object):
    def __init__(self, parts: List[str]):
        self.rock = defaultdict(lambda: '.')
        for r, row in enumerate(parts):
            for c, piece in enumerate(row):            
                self.rock[(r, c)] = piece

    def __repr__(self):
        m1, m2 = advent.minmax(*self.rock.keys())
        l = []
        for r in range(m1[0], m2[0]+1):
            l.append("".join(self.rock[(r, c)] for c in range(m1[1], m2[1] + 1)))
        return "\n".join(l)

def makerocks():
    with open("rocks.txt") as rf:
        data = list(r.rstrip() for r in rf.readlines())

    rockdata = []
    for row in data:
        if not row:
            yield Rock(rockdata)
            rockdata = []
        rockdata.append(row)
    yield Rock(rockdata)
       
class Tunnel(object):

    def __init__(self):
        self.fill = defaultdict(lambda: '.')

    def __getitem__(self, k):
        r = k[0]
        c = k[1]
        if c in (0, 8):
            if r == 0:
                return '+'
            return '|'
        if r == 0:
            return '-'
        return self.fill[k]

    def __setitem__(self, k, v):
        self.fill[k] = v

    def toString(self):
        m1, m2 = advent.minmax(*self.fill.keys())
        l = []
        for r in range(m1[0]-7, 1):
            l.append("".join(self[(r, c)] for c in range(0, 9)))
        return "\n".join(l)


def main():
    try:
        input = sys.argv[1]
    except IndexError:
            input = "input.txt"
    with open(input) as f:
        data = list(r.rstrip() for r in f.readlines())

    jet = data[0]

    rocks = makerocks()
    for r in rocks:
        print(" ")
        print(r)

    tunnel = Tunnel()
    tunnel[(-1, 1)] = '.'
    print(tunnel.toString())

if __name__ == '__main__':
    main()