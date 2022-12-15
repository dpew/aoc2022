#!/usr/bin/env python3

import sys
import os
import math
import pprint
from collections import defaultdict, deque
from functools import reduce
from typing import List, Dict, Any, Tuple

# create absolute mydir
mydir = os.path.abspath(os.path.dirname(__file__))
sys.path.append(os.path.join(mydir, '../lib'))

import advent

def intersection(pos: Tuple[int, int], dist: int, y: int) -> Tuple[int, int]:
    # print(f"pos={pos} dist={dist} y={y}")
    i = abs(pos[1] - y)
    if i > dist:
        return None
    d = dist - i
    return (pos[0] - d, pos[0] + d)
    


def main():
    try:
        input = sys.argv[1]
    except IndexError:
            input = "input.txt"
    with open(input) as f:
        data = list(l.rstrip() for l in f.readlines())

    distance = {}
    beacons = set()

    for row in data:
        l = list(advent.tokenize(row, ', :='))
        sensor=(int(l[3]),int(l[5]))
        beacon=(int(l[11]),int(l[13]))
        distance[sensor] = advent.mdistance(sensor, beacon)

    print(distance)
    m1, m2 = advent.minmax(*distance.keys())
    print((m1, m2))
    y1, y2 = m1[1], m2[1]
    for y in range(y1, y2+1):
        segments = []
        for sen in distance.keys():
            s = intersection(sen, distance[sen], y)
            # print(f"intersect={s}")
            if s:
                segments = advent.add_segment(segments, s)
            # print(f"segments={segments}")

        if len(segments) > 1:
            print(segments)
            x = segments[0][1] + 1
            print((x, y, x*4000000 + y))
            break
    

if __name__ == '__main__':
    main()