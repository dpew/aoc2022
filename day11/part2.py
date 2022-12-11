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

def plus(x, y):
    # print(f"plus {x} + {y}")
    return x + y

def mul(x, y):
    # print(f"mul  {x} * {y}")
    return x * y

OPERS = {
    '*': mul,
    '+': plus
}

class Monkey(object):
    def __init__(self):
        self.items = deque()
        self.operation = None
        self.test = None
        self.t = None
        self.f = None
        self.inspections = 0

    def __repr__(self):
        return f"Starting items: {self.items}\nOperation: X\nTest: divisible by {self.test}\nTrue: {self.t}\nFalse: {self.f}"

class Item(object):
    def __init__(self, *val):
        self.items = deque(val)

    def add(self, x):
        self.items.append(x)

    def val(self):
        return self.items[-1]

    def __repr__(self):
        return "item[" + ", ".join(str(x) for x in self.items) + "]"

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
                current.items.append(Item(int(i)))
        elif row.startswith('Operation'):
            oper = OPERS[r[4]]
            print(f"Oper {r[4]} {r[5]}")
            current.odesc = row[len("Operation: "):]
            if r[5] == 'old':
                # current.operation = lambda o: oper(o, o)   
                current.operation = lambda o,func=oper: func(o, o)
            else:
                val = int(r[5])
                print(f"Oper2 {r[4]} {val}")
                current.operation = lambda x,y=val,func=oper: func(x, y)
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

    print(type(monkies))
    seen = {}
    last = list(m.inspections for m in monkies)
    for r in range(240):
        for m in monkies:
            items = m.items
            m.items = deque()
            for i in items:                
                w = m.operation(i.val())
                i.add(w)
                # print(f"Item: {i} w {w}")
                # w = int(w / 3)
                # print(f"Item: {i} w {w}")
                if w % m.test == 0:
                    next, c = m.t, True
                else:
                    next, c = m.f, False
                # print(f"test {m.test} {w} {m.t} {m.f} {c} {next} {m.odesc}")
                monkies[next].items.append(i)
                m.inspections += 1
        print(f"Round {r}:")
        delta = tuple(m.inspections - last[e] for e, m in enumerate(monkies))
        seen[delta] = r
        for e, m in enumerate(monkies):
            # print(f"{e}: {m.items} {m.inspections}")
            print(f"{e}: {m} {m.inspections} {delta[e]}")
        
        last = list(m.inspections for m in monkies)

    i = [m.inspections for m in monkies]
    i.sort()
    print(i[-1] * i[-2])
        


if __name__ == '__main__':
    main()