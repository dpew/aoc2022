#!/usr/bin/env python3

import sys
import os
import math
import pprint
from collections import defaultdict, deque
from functools import reduce
from typing import List, Dict, Any

# create absolute mydir
mydir = os.path.abspath(os.path.dirname(__file__))
sys.path.append(os.path.join(mydir, '../lib'))

import advent

def main():
    try:
        input = sys.argv[1]
    except IndexError:
            input = "input.txt"
    with open(input) as f:
        data = list(l.rstrip() for l in f.readlines())

    grid = defaultdict(lambda: '.')
    grid[(500, 0)] = '+'

    def drawto(p1, p2):
        if p1[0] == p2[0]:
            y1, y2 = sorted((p1[1], p2[1]))
            for y in range(y1, y2 + 1):
                yield (p1[0], y)
        else:
            x1, x2 = sorted((p1[0], p2[0]))
            for x in range(x1, x2 + 1):
                yield (x, p1[1])

    for row in data:
        coords = advent.tokenize(row, ' ->')
        last = None
        for c in coords:
            next = tuple(int(x) for x in c.split(","))
            print(next)
            if last:
                for pos in drawto(last, next):
                    grid[pos] = '#'
            last = next

    print(list(grid.keys()))
    m1, m2 = advent.minmax(*list(grid.keys()))
    for x in range(m1[1], m2[1] + 1):
        print("".join(grid[(y, x)] for y in range(m1[0], m2[0] +1 )))

if __name__ == '__main__':
    main()