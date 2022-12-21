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

    def __repr__(self):
        return str(self.val)

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
        self.zero = None

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
        if n.val == 0:
            self.zero = n

    def navigate(self):
        begin = self.zero
        yield begin
        n = begin.next
        while n is not begin:
            yield n
            n = n.next

    def rnavigate(self):
        begin = self.zero
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

    def fastmove(self, n: Node, count: int = None):
        def moveto(n: Node, count: int):
            print(f"moveto(n={n}, count={count})")
            if count == 0:
                return
            # remove node
            prev = n.prev
            next = n.next
            prev.next = next
            next.prev = prev

            s = n.advance(count)

            # Insert before s
            sn = s.next
            s.next = n
            n.prev = s
            n.next = sn
            sn.prev = n
        if count is None:
            count = n.val
        if count == 0:
            return
        size = len(self.ordered)
        # if count > 0:
        moveto(n, (count % (size-1)))
        # else:
            # moveto(n, -((-count) % (size-1)))


def runtest():
    decryptkey = 299
    try:
        input = sys.argv[1]
    except IndexError:
            input = "input.txt"
    with open(input) as f:
        data = list(r.rstrip() for r in f.readlines())

    dl2 = DougList()
    dl3 = DougList()
    for d in data:
        dl2.append(int(d) * decryptkey)
        dl3.append(int(d) * decryptkey)

    print(dl2)
    size = len(dl2.ordered)
    for i in range(10):
        for e, n in enumerate(dl2.ordered):
            before = str(dl2)
            n3 = dl3.ordered[e]            
            dl2.fastmove(n)
            dl3.move(n3)
            if str(dl2) != str(dl3):
                raise ValueError(f"Failure at step {e} with {n}\nbefore={before}\nexpect={dl3}\n   got={dl2}")
            print(dl2)

    for n in dl2.ordered:
        if n.val == 0:
            zero = n
            break

    v1 = zero.advance(1000 % size).val
    v2 = zero.advance(2000 % size).val
    v3 = zero.advance(3000 % size).val

    print((v1, v2, v3, v1 + v2 + v3))

def puzzle():
    decryptkey = 811589153
    try:
        input = sys.argv[1]
    except IndexError:
            input = "input.txt"
    with open(input) as f:
        data = list(r.rstrip() for r in f.readlines())

    dl2 = DougList()
    for d in data:
        dl2.append(int(d) * decryptkey)

    size = len(dl2.ordered)
    for i in range(10):
        for n in dl2.ordered:
            dl2.fastmove(n)

    for n in dl2.ordered:
        if n.val == 0:
            zero = n
            break

    v1 = zero.advance(1000 % size).val
    v2 = zero.advance(2000 % size).val
    v3 = zero.advance(3000 % size).val

    print((v1, v2, v3, v1 + v2 + v3))


def main():
    try:
        input = sys.argv[1]
    except IndexError:
        input = "input.txt"
    with open(input) as f:
        data = list(r.rstrip() for r in f.readlines())

    test = False
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

    puzzle()

if __name__ == '__main__':
    main()