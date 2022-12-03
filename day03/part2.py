#!/usr/bin/env python3

import sys
from functools import reduce
from itertools import groupby

def main():
    with open('input.txt') as f:
        data = f.readlines()

    data = [ l.strip() for l in data ]

    def priority(c):
        if c >= 'a' and c <= 'z':
            return ord(c) - ord('a') + 1
        return ord(c) - ord('A') + 27

    print(data)
    sum = 0
    groups = []
    for k, g in groupby(enumerate(data), lambda e: int(e[0]/3)):
        groups.append(list([set(x[1]) for x in g]))

    sum = 0
    for g in groups:
        common = list(reduce(lambda a, b: a.intersection(b), g))[0]
        p = priority(common)
        print(f"{p} {common} {g}")
        sum += p

    print(sum)

    #     print(group)
    #     c1 = ruck[:int(len(ruck)/2)]
    #     c2 = ruck[len(c1):]
    #     print(f"c1={c1} c2={c2}")
    #     s = set(c1)
    #     m = list(s.intersection(c2))[0]
    #     p = priority(m)
    #     print(f"match {m} {p}")
    #     sum += p

    # print(sum)





if __name__ == '__main__':
    main()