#!/usr/bin/env python

import sys
import os
from collections import defaultdict, deque
from pprint import pprint
from typing import Dict

mydir = os.path.abspath(os.path.dirname(__file__))
sys.path.append(os.path.join(mydir, '../lib'))

import advent


DIRS = {
    'R': (1, 0),
    'L': (-1, 0),
    'U': (0, -1),
    'D': (0, 1)
}

def domove(head, tail):
    p0, p1 = head[0] - tail[0], head[1] - tail[1]
    if p0 == 0:
        return (p0, toward(p1))
    if p1 == 0:
        return (toward(p0), p1)
    if advent.mdistance(head, tail) > 2:
        return (absmax(p0), absmax(p1))
    return (0, 0)

def toward(v):
    if v > 0:
        return v-1
    if v < 0:
        return v + 1
    return v

def absmax(v):
    if v > 0 and v > 1:
        return 1
    if v < 0:
        return -1
    return v

def main():
    try:
        input = sys.argv[1]
    except IndexError:
        input = 'input.txt'

    visited = {}
    head = (0, 0)
    tail = (0, 0)
    visited[tail] = 1
    with open(input) as f:
        for move in ( d.rstrip() for d in f.readlines()):
            d, c = move.split(" ")
            c = int(c)
            inc = DIRS[d]
            for i in range(c):
                head = advent.addpos(head, inc)
                delta = domove(head, tail)
                tail = advent.addpos(tail, delta)
                pprint((head, tail, delta))
                visited[tail] = 1

    print(sum(visited.values()))

if __name__ == '__main__':
    main()

