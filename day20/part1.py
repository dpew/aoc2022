#!/usr/bin/env python3

import sys
import os
import math
import pprint
from collections import defaultdict, deque
from queue import PriorityQueue
from typing import List, Dict, Any, Tuple, FrozenSet, Iterator, Generator
from sys import maxsize
from itertools import cycle

# create absolute mydir
mydir = os.path.abspath(os.path.dirname(__file__))
sys.path.append(os.path.join(mydir, '../lib'))

import advent

class Node(object):
    def __init__(self, val: int):
        self.val = val
        self.next: Node = None
        self.prev: Node = None

def navigate(start: Node):
    n = start.next
    while n.val is not None:
        yield n
        n = n.next

def rnavigate(start: Node):
    n = start.prev
    while n.val is not None:
        yield n
        n = n.prev

def swapnext(n: Node):
    s = n.next
    last = s.next
    first = n.prev

    last.prev = n
    n.next = last

    first.next = s
    s.prev = first

    s.next = n
    n.prev = s

def swapprev(n: Node):
    s = n.prev

    first = s.prev
    last = n.next

    first.next = n
    n.prev = first

    last.prev = s
    s.next = last

    s.prev = n
    n.next = s

def move(n: Node):
    count = n.val
    if count > 0:
        for i in range(count):
            swapnext(n)
            if n.next.val == None:
                swapnext(n)
    else:
        for i in range(-count):
            swapprev(n)
            if n.prev.val == None:
                swapprev(n)

def indexof(n: Node, i: int, size: int):
    x = i % size
    
    for j in range(x):
        n = n.next
        if n.val is None:
            n = n.next
    return n.val


def main():
    try:
        input = sys.argv[1]
    except IndexError:
            input = "input.txt"
    with open(input) as f:
        data = list(r.rstrip() for r in f.readlines())

    n = Node(None)
    n.next = n
    n.prev = n
    start = n

    ordered = []
    for d in data:
        nn = Node(int(d))
        nn.next = n.next
        nn.next.prev = nn
        nn.prev = n
        n.next = nn
        ordered.append(nn)
        n = nn


    print(", ".join(str(nv.val) for nv in ordered))    
    print(", ".join(str(nv.val) for nv in navigate(start)))
    print(", ".join(str(nv.val) for nv in rnavigate(start)))

    def printit():
        print(", ".join(str(nv.val) for nv in navigate(start)))

    for n in ordered:
        print(f"Move {n.val}")
        move(n)
        # printit()

    for n in ordered:
        if n.val == 0:
            zero = n
            break

    size = len(ordered)
    v1 = indexof(zero, 1000, size)
    v2 = indexof(zero, 2000, size)
    v3 = indexof(zero, 3000, size)

    print((v1, v2, v3, v1 + v2 + v3))

if __name__ == '__main__':
    main()