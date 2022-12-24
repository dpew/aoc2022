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


class Monkey:

    def __init__(self, name: str, m1: str, m2: str, func, m1func, m2func):
        self.name = name
        self.m1 = m1
        self.m2 = m2
        self.func = func
        self.m1func = m1func
        self.m2func = m2func

    def emit(self, name: str, values: Dict[str, int]) -> int:
        '''
            Returns value if solved, else None
        '''
        if self.m1 in values and self.m2 in values:
            return self.func(values[self.m1], values[self.m2])
        return None

    def solve(self, val: int, values: Dict[str, int]) -> str:
        '''
            Returns the name of the unknown value that is now solved
        '''
        if self.m1 not in values:
            values[self.m1] = self.m1func(val, values[self.m2])
            return self.m1
        elif self.m2 not in values:
            values[self.m2] = self.m2func(val, values[self.m1])
            return self.m2

def main():
    try:
        input = sys.argv[1]
    except IndexError:
            input = "input.txt"
    with open(input) as f:
        data = list(r.rstrip() for r in f.readlines())

    values = {}
    monkies = {}

    def tellmonkies(name: str):
        for m in monkies.values():
            val = m.emit(name, values)
            if val is not None:
                values[m.name] = val
                del monkies[m.name]
                tellmonkies(m.name)
                break

    for row in data:
        dx = list(advent.tokenize(row, ': '))
        if len(dx) == 2:
            if dx[0] == 'humn':
                continue
            values[dx[0]] = int(dx[1])
            tellmonkies(dx[0])
        else:
            name, m1, oper, m2 = dx
            if oper == '*':
                func = lambda x, y: x*y
                m1func = lambda r, y: int(r / y)
                m2func = m1func
            elif oper == '+':
                func = lambda x, y: x+y
                m1func = lambda r, y: r - y
                m2func = m1func
            elif oper == '-':
                func = lambda x, y: x-y
                m1func = lambda r, y: r + y
                m2func = lambda r, x: x - r
            elif oper == '/':
                func = lambda x, y: int(x/y)
                m1func = lambda r, y: r * y
                m2func = lambda r, x: int(x / r)
            else:
                raise ValueError("unknown op " + oper)
            if name == 'root':
                func = lambda x, y: ValueError("bad")
                m1func = lambda r, y: y
                m2func = lambda r, x: x
            m = Monkey(name, m1, m2, func, m1func, m2func)
            val = m.emit(name, values)
            if val is not None:
                values[name] = val
            else:
                monkies[name] = m

    msize = len(monkies)
    changed = True
    while changed:
        tellmonkies('whatever')
        oldsize = msize
        msize = len(monkies)
        changed = bool(oldsize != msize)
        print((changed, oldsize, msize))

    solveFor = 'root' 
    values['root'] = 0 # Does not matter the value
    while solveFor != 'humn':
        solveFor = monkies[solveFor].solve(values[solveFor], values)
    
    print(values['humn'])

if __name__ == '__main__':
    main()
