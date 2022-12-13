#!/usr/bin/env python3

import sys
import os
import math
import pprint
from collections import defaultdict, deque
from queue import PriorityQueue
from typing import List, Dict, Any, Tuple

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
        data = list(f.readlines())

    grid = defaultdict(lambda: ' ')
    start = (0, 0)
    dest = (0, 0)
    maxgrid = (0, 0)

    for r, row in enumerate(data):
        for c, e in enumerate(row.rstrip()):
            pos = (r, c)
            maxgrid = (max(maxgrid[0], r), max(maxgrid[1], c))
            grid[pos] = e
            if e == 'S':
                start = pos
            elif e == 'E':
                dest = pos

    distance = defaultdict(lambda: 1000000)
    distance[start] = 0
    seen = set()
    seen.add(start)
    Q = set()
    Q.add(start)    

    def popmin():
        # print(f"POPMIN Q={Q}")
        next = min(Q, key=lambda v: distance[v])
        Q.remove(next)
        # print(f"POPMIN {next} {Q}")
        return distance[next], next


    def neighbors(pos: Tuple[int, int]) -> Tuple[int, Tuple[int, int]]:
        myalt = grid[pos]
        for p in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            np = advent.addpos(pos, p)
            if np in seen:
                continue
            if np not in grid:
                continue
            if myalt == 'S':
                yield 1, np
            x = grid[np]
            if x == 'E':
                x = 'z'
            if (myalt == 'S' or myalt == 'a') and x == 'a':
                yield 0, np
            delta = ord(x) - ord(myalt)
            if delta > 1:
                continue
            yield 1, np

    while Q:
        d, next = popmin()
        seen.add(next)
        print(f"STEP d={d} next={next}")
        for c, n in neighbors(next):
            print(f"{grid[n]}: d={c+d} n={n}")
            if c+d < distance[n]:
                distance[n] = c+d
                Q.add(n)
                if n == dest:
                    break

    print(distance[dest])
    # for r in range(maxgrid[0]+1):
    #     print(''.join(grid[(r,c)] for c in range(maxgrid[1]+1)))

    def pval(p):
        d = distance[p]
        if d > 1000:
            return "%s:  -" % (grid[p], )
        return "%s: %2d" % (grid[p], d)
    # for r in range(maxgrid[0]+1):
    #     print(' '.join( pval((r,c)) for c in range(maxgrid[1]+1)))

    
if __name__ == '__main__':
    main()