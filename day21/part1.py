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

    def __init__(self, name: str, m1: str, m2: str, func):
        self.name = name
        self.m1 = m1
        self.m2 = m2
        self.func = func

    def emit(self, name: str, values: Dict[str, int]) -> int:
        '''
            Returns value if solved, else None
        '''
        if self.m1 in values and self.m2 in values:
            return self.func(values[self.m1], values[self.m2])
        return None

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
            values[dx[0]] = int(dx[1])
            tellmonkies(dx[0])
        else:
            name, m1, oper, m2 = dx
            if oper == '*':
                func = lambda x, y: x*y
            elif oper == '+':
                func = lambda x, y: x+y
            elif oper == '-':
                func = lambda x, y: x-y
            elif oper == '/':
                func = lambda x, y: int(x/y)
            else:
                raise ValueError("unknown op " + oper)
            m = Monkey(name, m1, m2, func)
            val = m.emit(name, values)
            if val is not None:
                values[name] = val
            else:
                monkies[name] = m

    while monkies:
        tellmonkies('whatever')

    print(values['root'])

if __name__ == '__main__':
    main()
