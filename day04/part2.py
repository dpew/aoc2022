#!/usr/bin/env python
import sys
import os
# create absolute mydir
mydir = os.path.abspath(os.path.dirname(__file__))
sys.path.append(os.path.join(mydir, '../lib'))

import advent

def parse_range(s):
    a,b,c,d = (int(x) for x in advent.tokenize(s, '-,'))
    return (a,b),(c,d)

def within(x, v):
    'x is within v[0] [v]'
    return x >= v[0] and x <= v[1]

def overlap(v1, v2):
    'v1 intersects v2'
    return within(v1[0], v2) or within(v1[1], v2)


def main():
    try:
        input = sys.argv[1]
    except IndexError:
        input = 'input.txt'

    with open(input) as f:
        data = [d.strip() for d in f.readlines()]


    ccount = 0
    for d in data:
        range1, range2 = parse_range(d)
        if overlap(range1, range2) or overlap(range2, range1):
            print("%d-%d,%d,%d" % (range1[0], range1[1], range2[0], range2[1]))
            ccount += 1

    print(ccount)


if __name__ == '__main__':
    main()
