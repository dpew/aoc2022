#!/usr/bin/env python3

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

JET = {'<': (0, -1),
       '>': (0, 1)}

DOWN = (1, 0)



class Rock(object):
    def __init__(self, name: str, parts: List[str]):
        self.name = name
        self.rock = defaultdict(lambda: '.')
        for r, row in enumerate(parts):
            for c, piece in enumerate(row):            
                self.rock[(r, c)] = piece

        m1, m2 = advent.minmax(*self.rock.keys())
        self.size = tuple(x+1 for x in m2)

    def __getitem__(self, k):
        return self.rock[k]

    def __repr__(self):
        m1, m2 = advent.minmax(*self.rock.keys())
        l = []
        for r in range(m1[0], m2[0]+1):
            l.append("".join(self.rock[(r, c)] for c in range(m1[1], m2[1] + 1)))
        return "\n".join(l)

def makerocks():
    with open("rocks.txt") as rf:
        data = list(r.rstrip() for r in rf.readlines())

    rockdata = []
    for row in data:
        if row.startswith('name='):
            name=row[5]
            continue
        if not row:
            yield Rock(name, rockdata)
            rockdata = []
        else:
            rockdata.append(row)
    yield Rock(name, rockdata)

class Jetter(object):
    def __init__(self, jetstr: str):
        self.pos = 0
        self.cycle = 0
        self.jetstr = jetstr

    def next(self) -> str:
        v = self.jetstr[self.pos]
        self.pos = (1 + self.pos) % len(self.jetstr)
        if self.pos == 0:
            self.cycle += 1
        return v

class Tunnel(object):

    def __init__(self):
        self.fill = defaultdict(lambda: '.')
        self.top = 0

    def __getitem__(self, k):
        r = k[0]
        c = k[1]
        if c in (0, 8):
            if r == 0:
                return '+'
            return '|'
        if r == 0:
            return '-'
        return self.fill[k]

    def __setitem__(self, k, v):
        r = k[0]
        self.top = min(r, self.top)
        self.fill[k] = v

    def valueAt(self, r):
        v = 0
        for c in range(1, 8):
            x = self.fill[(r, c)]
            xv = 0 if x == '.' else 1
            v = (v<<1) + xv
        return v
    
    def values(self):
        for r in  range(-1, self.top-1, -1):
            yield self.valueAt(r)

    def lastValues(self, count: int):
        return tuple(self.valueAt(r) for r in range(self.top + count-1, self.top-1, -1))

    def toString(self):
        l = []
        for r in range(self.top-7, 1):
            l.append("".join(self[(r, c)] for c in range(0, 9)))
        return "\n".join(l)

def collides(tunnel: Tunnel, rock: Rock, offset: Tuple[int]):
    for r in range(0, rock.size[0]):
        for c in range(0, rock.size[1]):
            rpos = (r, c)
            tpos = (r + offset[0], c + offset[1])
            rp = rock[rpos]
            tp = tunnel[tpos]
            if rp != '.' and tp != '.':
                return True

    return False


def droprock(tunnel: Tunnel, rock: Rock, jet: Jetter):
    rpos = (tunnel.top - rock.size[0] - 3,  3)
    dropped = True
    while dropped:
        lastpos = rpos
        j = jet.next()
        wind = JET[j]
        npos = advent.addpos(rpos, wind)
        if not collides(tunnel, rock, npos):
            # print(f"{rpos}: Rock {rock.name} moved {wind} {j}")
            rpos = npos
        # else:
            # print(f"Rock {rock.name} blocked from wind {wind} {j}")
        dpos = advent.addpos(DOWN, rpos)
        if not collides(tunnel, rock, dpos):
            # print(f"{rpos}: Rock {rock.name} dropped")
            rpos = dpos
        else:
            dropped = False

    # rock stopped, add items to tunnel
    for r in range(0, rock.size[0]):
        for c in range(0, rock.size[1]):
            tpos = (rpos[0] + r, rpos[1] + c)
            rrpos = (r, c)
            if rock[rrpos] != '.':
                tunnel[tpos] = rock[rrpos]

def main():
    try:
        input = sys.argv[1]
    except IndexError:
            input = "input.txt"
    with open(input) as f:
        data = list(r.rstrip() for r in f.readlines())

    jet = data[0]

    rocks = list(makerocks())
    for r in rocks:
        print(" ")
        print(r)
        print(r.size)

    tunnel = Tunnel()
    print(tunnel.toString())
    
    times = 2022
    # times = 5
    jetgen = Jetter(jet)
    repeat = advent.Repeat()
    i: int = 0
    heights: Dict[int, int] = {}
    while not repeat.found:
    # for i in range(times):
        rnum = i % len(rocks)
        droprock(tunnel, rocks[rnum], jetgen)
        # print(tunnel.toString())
        signature =(jetgen.pos,  rnum, tunnel.lastValues(20)) 
        repeat.see(signature)
        heights[i] = tunnel.top
            
        i += 1
        # print(tunnel.lastValues(20))
        
    print(f"i={i} jetpos={jetgen.pos} jetcycle={jetgen.cycle}")
    print(tunnel.lastValues(20))
    print(repeat)
    print(signature)
    h1 = -heights[repeat.start]
    h2 = -heights[repeat.end]
    delta = h2 - h1
    deltai = repeat.end - repeat.start
    print(f"Height1: {h1} Height2: {h2} Delta: {delta} DeltaI: {deltai}")
    print(tunnel.top)

    rockcount = 1000000000000
    repeatCount = int((rockcount - repeat.start) / deltai)
    remainder = (rockcount - repeat.start) % deltai
     
    ntunnel = Tunnel()
    jetgen = Jetter(jet)
    totalRemaining = repeat.start + remainder
    for i in range(totalRemaining):
    # for i in range(times):
        droprock(ntunnel, rocks[i % len(rocks)], jetgen)

    print(f"remaining: {totalRemaining} remainder: {remainder} top: {ntunnel.top}")

    total = (delta * repeatCount) - ntunnel.top
    print(total)


if __name__ == '__main__':
    main()