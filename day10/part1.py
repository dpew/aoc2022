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

    global cycles
    global X
    X = 1
    cycles = 0
    check = (20, 60, 100, 140, 180, 220)
    global total
    total = 0

    def accum():
        global total
        global cycles
        global X
        if cycles in check:
            total += (cycles * X)
            print((cycles, X))

    with open(input) as f:
        for line in ( d.rstrip() for d in f.readlines()):
            instr = line.split(" ")
            print(instr)
            if instr[0] == 'noop':
                cycles += 1
                accum()
            elif instr[0] == 'addx':
                cycles += 1
                accum()
                cycles += 1
                accum()
                val = int(instr[1])
                X += val

    print(total)

if __name__ == '__main__':
    main()

