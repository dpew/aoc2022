#!/usr/bin/env python


import sys

def main():
    with open('input.txt') as f:
        data = list(d.strip() for d in f.readlines())


    elves = [0]
    for cal in data:
        if not cal:
            elves.append(0)
            continue
        elves[-1] += int(cal)

    print(elves)
    top = list(sorted(elves))[-3:]
    print(top)
    print(sum(top))


if __name__ == '__main__':
    main()
