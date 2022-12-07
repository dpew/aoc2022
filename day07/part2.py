#!/usr/bin/env python

import sys
import os
from collections import defaultdict, deque
from pprint import pprint
from typing import Dict

mydir = os.path.abspath(os.path.dirname(__file__))
sys.path.append(os.path.join(mydir, '../lib'))

import advent


class File(object):
    def __init__(self, size: int, name: str):
        self._size = size
        self.name = name

    def size(self):
        return self._size

class Dir(File):
    def __init__(self, name: str):
        self._files = deque()
        self.parent = None
        self.name = name
        self._size = None

    def add(self, file: File): 
        self._files.append(file)
        file.parent = self

    def getdir(self, name):
        if name == '..':
            return self.parent
        for f in self._files:
            if f.name == name:
                return f
        raise KeyError(name)
    
    def size(self) -> int:
        if self._size is None:
            s = 0
            for f in self._files:
                s2 = f.size()
                # print(f"{s2} {f.name}")
                s += s2
            self._size = s
        return self._size

    def list(self):
        return self._files

def findless(d: Dir, size: int):
    for f in d.list():
        print((f.name, f.size()))
        if not isinstance(f, Dir):
            continue
        if f.size() <= size:
            print(f"FOUND {f.name}")
            yield f
        yield from findless(f, size)

def findmore(d: Dir, size: int):
    for f in d.list():
        print((f.name, f.size()))
        if not isinstance(f, Dir):
            continue
        if f.size() >= size:
            print(f"FOUND {f.name}")
            yield f
        yield from findmore(f, size)

def main():
    try:
        input = sys.argv[1]
    except IndexError:
        input = 'input.txt'

    root = Dir("/")
    cwd = root

    with open(input) as f:
        for line in [ d.rstrip() for d in f.readlines()]:
            args = line.split(' ')
            if args[0] == '$' and args[1] == 'cd':
                if args[2] == '/':
                    cwd = root
                else:
                    cwd = cwd.getdir(args[2])             
            elif args[0] == '$' and args[1] == 'ls':
                pass
            elif args[0] == 'dir':                
                cwd.add(Dir(args[1]))
            else:
                cwd.add(File(int(args[0]), args[1]))

    print(root.size())
    sums = 0
    for d in findless(root, 100000):
        s = d.size()
        print(f"{s} {d.name}")
        sums += s
    print(sums)

    total = 70000000
    required = 30000000
    free = total - root.size()

    todel = required - free

    sizes=[]
    for d in findmore(root, todel):
        sizes.append(d.size())

    print(min(sizes))



    

if __name__ == '__main__':
    main()

