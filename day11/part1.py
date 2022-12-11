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
OPERS = {
    '*': lambda o, n: o * n,
    '+': lambda o, n: o + n
}

class Monkey(object):
    def __init__(self):
        self.items = deque()
        self.operation = None        
        self.test = None
        self.t = None
        self.f = None

    def __repr__(self):
        return f"Starting items: {self.items}\nOperation: X\nTest: divisible by {self.test}\nTrue: {self.t}\nFalse: {self.f}"

def parse(data: List[str]) -> List[Dict[str, Any]]:
    monkies = []
    current = None
    for row in data:
        row = row.strip()
        r = row.split(' ')
        if row.startswith('Monkey'):
            current = Monkey()
            monkies.append(current)
        elif row.startswith('Starting'):
            for i in r[2:]:
                if i.endswith(','):
                    i = i[:-1]
                current.items.append(int(i))
        elif row.startswith('Operation'):
            oper = OPERS[r[4]]
            if r[5] == 'old':
                current.operation = lambda o: oper(o, o)
            else:
                current.operation = lambda o: oper(o, int(r[5]))
        elif row.startswith('Test'):
            current.test = int(r[3])
        elif row.startswith('If'):
            if r[1] == 'true:':
                current.t = int(r[5])
            if r[1] == 'false:':
                current.f = int(r[5])

    return monkies
        

def main():
    try:
        input = sys.argv[1]
    except IndexError:
            input = "input.txt"
    with open(input) as f:
        data = list(f.readlines())

    monkies = parse(data)
    pprint.pprint(monkies)


if __name__ == '__main__':
    main()