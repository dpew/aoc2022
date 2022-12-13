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
        data = list(f.readlines())

    grid = defaultdict(lambda: ' ')
    start = (0, 0)
    dest = (0, 0)

    for r, row in enumerate(data):
        for c, e in row.rstrip():
            pos = (r, c)
            grid[(r, c)] = e
            if e == 'S':
                start = pos
            elif e == 'E':
                dest = pos

    min = 1e7
    mypos = start

    for v in neighbors(mypos):
        if 


if __name__ == '__main__':
    main()