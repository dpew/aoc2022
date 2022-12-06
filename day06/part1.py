#!/usr/bin/env python

import sys
import os
from collections import defaultdict, deque
from pprint import pprint
from typing import Dict

mydir = os.path.abspath(os.path.dirname(__file__))
sys.path.append(os.path.join(mydir, '../lib'))

import advent

class Code:

    def __init__(self):
        self.code = deque()
        self.msg = ''
    
    def append(self, c):
        self.code.append(c)
        if len(self.code) > 4:
            self.code.popleft()
        self.msg = ''.join(self.code)

    def valid(self):
        return len(set(self.code)) == 4

    def __repr__(self):
        return f"msg={self.msg} {self.valid()}"


def process(data):
    print(data)
    code = Code()
    for e, c in enumerate(data):
        code.append(c)
        print(code)
        if code.valid():
            print(e + 1)
            break

def main():
    try:
        input = sys.argv[1]
    except IndexError:
        input = 'input.txt'

    with open(input) as f:
        for data in f.readlines():
            process(data.rstrip())

if __name__ == '__main__':
    main()

