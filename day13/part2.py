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

def parselist(s: str) -> List[List[Any]]:
    thelist = []
    stack = []

    val = ''
    for c in s:
        if c == '[':
            if val:
                thelist.append(int(val))
                val = ''
            stack.append(thelist)
            thelist.append([])
            thelist = thelist[-1]
        elif c == ']':
            if val:
                thelist.append(int(val))
                val = ''
            thelist = stack.pop()
        elif c >= '0' and c <= '9':
            val = val + c
        elif c == ',':
            if val:
                thelist.append(int(val))
                val = ''
    return thelist


def compare(l1: List[Any], l2: List[Any]) -> int:
    if isinstance(l1, int) and isinstance(l2, int):
        return l1 - l2
    if isinstance(l1, int):
        l1 = [l1]
    if isinstance(l2, int):
        l2 = [l2]

    for t in zip(l1, l2):
        c = compare(*t)
        if c != 0:
            return c
    return len(l1) - len(l2)

def dosum(l1: List[int]):
    if isinstance(l1, int):
        return l1
    s = 0
    for s1 in l1:
        s += dosum(s1)
    return s

def main():
    try:
        input = sys.argv[1]
    except IndexError:
            input = "input.txt"
    with open(input) as f:
        data = list(f.readlines())

    data.append('')
    data.append('[[2]]')
    data.append('[[6]]')

    packets = []
    for i in range(0, len(data),3):
        packets.append(parselist(data[i]))
        packets.append(parselist(data[i+1]))

    from functools import cmp_to_key
    spackets = sorted(packets, key=cmp_to_key(compare))
    # pprint.pprint(spackets)

    i1 = spackets.index([[[2]]])+1
    i2 = spackets.index([[[6]]])+1


    print(i1 * i2)

if __name__ == '__main__':
    main()