#!/usr/bin/env python3

import sys

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
    for ruck in data:
        c1 = ruck[:int(len(ruck)/2)]
        c2 = ruck[len(c1):]
        print(f"c1={c1} c2={c2}")
        s = set(c1)
        m = list(s.intersection(c2))[0]
        p = priority(m)
        print(f"match {m} {p}")
        sum += p

    print(sum)





if __name__ == '__main__':
    main()