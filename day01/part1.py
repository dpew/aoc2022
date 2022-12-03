#!/usr/bin/env python


import sys

def main():
    with open('input.txt') as f:
        data = list(d.strip() for d in f.readlines())


    elves = []
    cals = 0
    for cal in data:
        if not cal:
            elves.append(cals)
            cals = 0
            continue
        cals += int(cal)

    print(elves)
    print(max(elves))


if __name__ == '__main__':
    main()
