#!/usr/bin/env python3

from __future__ import annotations

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

    def advance(self, count: int) -> Node:
        n = self
        if count >= 0:
            for i in range(count):
                n = n.next
                if n.val == None:
                    n = n.next
        else:
            for i in range(-count):
                n = n.prev
                if n.val == None:
                    n = n.prev
        print(f"find({self.val}, {count}) -> {n.val}")
        return n

    def swapnext(self):
        n = self
        s = n.next
        last = s.next
        first = n.prev

        last.prev = n
        n.next = last

        first.next = s
        s.prev = first

        s.next = n
        n.prev = s

    def swapprev(self):
        n = self
        s = n.prev
        first = s.prev
        last = n.next

        first.next = n
        n.prev = first

        last.prev = s
        s.next = last

        s.prev = n
        n.next = s

class DougList(object):
    def __init__(self):
        self.start = None
        self.ordered = []

    def append(self, val: int):
        n = Node(val)
        if self.start is None:
            self.start = n
            n.next = n
            n.prev = n
        else:
            n.next = self.start
            n.prev = self.start.prev
            n.prev.next = n
            self.start.prev = n

        self.ordered.append(n)

    def navigate(self):
        yield self.start
        n = self.start.next
        while n is not self.start:
            yield n
            n = n.next

    def rnavigate(self):
        begin = self.start.prev
        yield begin
        n = begin.prev
        while n is not begin:
            yield n
            n = n.prev

    def __repr__(self):
        return ", ".join(str(nv.val) for nv in self.navigate())

    def move(self, n: Node):
        count = n.val
        if count > 0:
            for i in range(count):
                n.swapnext()
        else:
            for i in range(-count):
                n.swapprev()


def moveto(n: Node, count: int):
    if count < 0:
        count -= 1
    s = findnext(n, count)
    if s.val == 42 and n.val == 4999:
        print(f"snv={s.next.val} spv={s.prev.val} nnv={n.next.val} npv={n.prev.val}" )

    if s == n:
        print("SAME")
        return
    if n.next == s:
        print("MOVE NEXT")
    if n.prev == s:
        print("MOVE PREV")
        return
    else:
        safter = s.next
        sbefore = s.prev

        nafter = n.next
        nbefore = n.prev

        nafter.prev = nbefore
        nbefore.next = nafter
        # if count > 0:
        s.next = n
        n.prev = s

        n.next = safter
        safter.prev = n
    # else:
    #     s.prev = n
    #     n.next = s

    #     n.prev = sbefore
    #     sbefore.next = n

def moveit(n: Node, count: int, size: int):    
    if count == 0:
        pass
    # elif count == 1:
    #     swapnext(n)
    #     if n.next.val == None:
    #         swapnext(n)
    # elif count == -1:
    #     swapprev(n)
    #     if n.prev.val == None:
    #         swapprev(n)
    elif count > 0:
        moveto(n, count % size)
    else:
        moveto(n, -((-count)%size))

def move(start: Node, n: Node, size: int):
    before = doprint(n)
    moveit(n, n.val, size)
    middle = doprint(n)
    moveit(n, -n.val, size)
    after = doprint(n)
    if before != after:
        raise ValueError(f"We have a problem moving {n.val} size={size}\nb=[{before}]\nm=[{middle}]\na=[{after}]")
    moveit(n, n.val, size)

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

    test = True
    if test:
        dl = DougList()

        for d in data:
            dl.append(int(d))


        print(", ".join(str(nv.val) for nv in dl.ordered))    
        print(", ".join(str(nv.val) for nv in dl.navigate()))
        print(", ".join(str(nv.val) for nv in dl.rnavigate()))

        size = len(dl.ordered)
        for n in dl.ordered:
            # print(f"Move {n.val}")
            dl.move(n)
            # print(dl)
        print(dl)

        for n in dl.ordered:
            if n.val == 0:
                zero = n
                break

        v1 = zero.advance(1000 % size).val
        v2 = zero.advance(2000 % size).val
        v3 = zero.advance(3000 % size).val

        print((v1, v2, v3, v1 + v2 + v3))
        sys.exit(1)

    decryptkey = 811589153
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
        nn = Node(int(d) * decryptkey)
        nn.next = n.next
        nn.next.prev = nn
        nn.prev = n
        n.next = nn
        ordered.append(nn)
        n = nn

    size = len(ordered)
    printit()
    for i in range(10):
        for n in ordered:
            # print(f"Move {n.val}")
            move(start, n, size)
        printit()

    for n in ordered:
        if n.val == 0:
            zero = n
            break

    v1 = indexof(zero, 1000, size)
    v2 = indexof(zero, 2000, size)
    v3 = indexof(zero, 3000, size)

    print((v1, v2, v3, v1 + v2 + v3))


if __name__ == '__main__':
    main()