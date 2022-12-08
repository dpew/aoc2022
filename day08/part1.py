#!/usr/bin/env python

import sys
import os
from collections import defaultdict, deque
from pprint import pprint
from typing import Dict

mydir = os.path.abspath(os.path.dirname(__file__))
sys.path.append(os.path.join(mydir, '../lib'))

import advent


def main():
    try:
        input = sys.argv[1]
    except IndexError:
        input = 'input.txt'

    trees = {}
    with open(input) as f:
        for r, row in enumerate( d.rstrip() for d in f.readlines()):
            for c, t in enumerate(row):
                trees[(r, c)] = int(t)

    # print(trees)

    count = 0
    for pos in list(trees.keys()):
        hi = False
        
        for p in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            
            np = advent.addpos(pos, p)            
            while True:
                if np not in trees:              
                    hi = True
                    break
                elif trees[pos] <= trees[np]:
                    break
                np = advent.addpos(np, p)
        if hi:
            count += 1
        # if not edge:
        #     print((hi, pos, trees[pos]))

    print(count)

if __name__ == '__main__':
    main()

