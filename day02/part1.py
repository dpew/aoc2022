#!/usr/bin/env python
import sys

LOOKUP = {
        'A': 'R',
        'B': 'P',
        'C': 'S',
        'X': 'R',
        'Y': 'P',
        'Z': 'S'
        }

POINTS = { 'R': 1,
          'P': 2,
          'S': 3 }

BEAT = {'P': 'R',
        'S': 'P',
        'R': 'S'}

def compare(i1, i2):
    if i1 == i2:
        return 3
    if BEAT[i1] == i2:
        return 0
    return 6

def rps(them, us):
    ti = LOOKUP[them]
    ui = LOOKUP[us]
    score = POINTS[ui]
    score += compare(ti, ui)
    return score


def main():
    try:
        input = sys.argv[1]
    except IndexError:
        input = 'sample.txt'
    with open(input) as f:
        data = list(d.strip() for d in f.readlines())


    total = 0
    for play in data:
        t, u = play.split(' ')

        score = rps(t, u)
        total += score
        print(f"{t} {u} {score} {total}")

if __name__ == '__main__':
    main()
