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
    print(f"pos={pos} dist={dist} y={y}")
    i = abs(pos[1] - y)
    if i > dist:
        return None
    d = dist - i
    return (pos[0] - d, pos[0] + d)
    


def main():

    try:
        y = int(sys.argv[2])
    except (IndexError, ValueError):
        y = 2000000

    try:
        input = sys.argv[1]
    except IndexError:
            input = "input.txt"
    with open(input) as f:
        data = list(l.rstrip() for l in f.readlines())

    distance = {}
    beacons = set()
    beaconsAtY = 0

    for row in data:
        l = list(advent.tokenize(row, ', :='))
        sensor=(int(l[3]),int(l[5]))
        beacon=(int(l[11]),int(l[13]))
        distance[sensor] = advent.mdistance(sensor, beacon)
        if beacon not in beacons:
            beacons.add(beacon)
            if beacon[1] == y:
                beaconsAtY += 1

    print(distance)
    segments = []
    for sen in distance.keys():
        s = intersection(sen, distance[sen], y)
        print(f"intersect={s}")
        if s:
            segments = advent.add_segment(segments, s)
        print(f"segments={segments}")
    
    gaps = 0
    for i in range(len(segments)-1):
        g = segments[i+1][0] - segments[i][1]
        gaps += g 

    notcount = 0
    for seg in segments:
        c = seg[1] - seg[0] + 1
        notcount += c

    print(f"notcount={notcount} beaconsAtY={beaconsAtY}")
    print(notcount-beaconsAtY)

if __name__ == '__main__':
    main()