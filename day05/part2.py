#!/usr/bin/env python

import sys
import os
from collections import defaultdict, deque
from pprint import pprint
from typing import Dict

mydir = os.path.abspath(os.path.dirname(__file__))
sys.path.append(os.path.join(mydir, '../lib'))

import advent

def parse_stacks(data: str) -> Dict[int, deque]:
    stacks = defaultdict(lambda: deque())
    finalstacks = {}
    for r in data:
        if finalstacks:
            return finalstacks
        f = False
        for c, x in enumerate(r):
            print((f, c, x))
            pprint(finalstacks)
            pprint(stacks)            
            try:
                col = int(x)
                finalstacks[col] = stacks[c]
                finalstacks[col].reverse()
            except ValueError:
                pass
            if f:
                stacks[c].append(x)
            f = x == '['

def parse_moves(data: str):
    for r in data:
        if r.startswith('move'):
            m = list(advent.tokenize(r))
            yield int(m[1]), int(m[3]), int(m[5])
    

def main():
    try:
        input = sys.argv[1]
    except IndexError:
        input = 'input.txt'

    with open(input) as f:
        data = [d.rstrip() for d in f.readlines()]

    stacks = parse_stacks(data)
    pprint(("STACKS", stacks))
    for count, f, t in parse_moves(data):
        print((count, f, t))
        pprint(stacks)
        boxes = []
        for x in range(count):
            pprint(stacks[f])
            pprint(stacks[t])
            boxes.append(stacks[f].pop())
        for b in boxes[::-1]:
            stacks[t].append(b)
    pprint(stacks)
 
    tops = []
    for k in sorted(stacks.keys()):
        tops.append(stacks[k].pop())
    print(''.join(tops))
        
            


     
if __name__ == '__main__':
    main()