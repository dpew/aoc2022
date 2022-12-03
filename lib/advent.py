#!/usr/bin/env python

import itertools
import math


def mdistance(p1, p2):
    '''
        Manhattan Distance

        Gives an absolute value of the manhattan distance of two nodes. Each node may have N dimensions.

        >>> mdistance((8, 9), (8, 9))
        0
        >>> mdistance((8, 9), (9, 9))
        1
        >>> mdistance((8, 9), (9, 10))
        2
        >>> mdistance((8, 9), (9, 7))
        3
        >>> mdistance((8, 9, 10), (9, 7, 5))
        8
        >>> mdistance(xrange(5), xrange(1, 6))
        5
        >>> mdistance((10, 10, 10), (12, 12, 12))
        6
    '''
    return sum(abs(p[0] - p[1]) for p in zip(p1, p2))


def tokenize(s, chars=' '):
    '''
        >>> list(tokenize('pos=<-22356506,24819383,19709017>, r=53389427', 'pos=<,>r= '))
        ['-22356506', '24819383', '19709017', '53389427']
        >>> list(tokenize(' 1234  1 abc3 '))
        ['1234', '1', 'abc3']
        >>> list(tokenize(' 1234  1 abc3 ', 'abc '))
        ['1234', '1', '3']
    '''
    found = []
    for c in s:
        if c not in chars:
            found.append(c)
        else:
            if found:
                yield ''.join(found)
                found = []
    if found:
       yield ''.join(found)

def addpos(*positions):
    '''
       >>> addpos((1, 2), (1, 2))
       (2, 4)
       >>> addpos((1, 2, 3), (1, 2, 4))
       (2, 4, 7)
       >>> addpos((1, 2, 3), (1, 2, 4), (-2, -4, -7))
       (0, 0, 0)
    '''
    return tuple((sum(p[x] for p in positions) for x in range(len(positions[0]))))

def invertpos(p):
    return tuple(-x for x in p)

def subpos(p1, p2):
    return addpos(p1, invertpos(p2))

def mulpos(v, p):
    '''
       >>> mulpos((0, 1, 2, 3), 2)
       (0, 2, 4, 6)
    '''
    return mapvector(lambda x: p * x, v)

def mintuple(t1, t2):
    '''
        >>> mintuple((-4, 10, 8), (-100, 12, 19))
        (-100, 10, 8)
        >>> mintuple((-4, 10), (-100, 12))
        (-100, 10)
    '''
    return tuple(min(x) for x in zip(t1, t2))

def maxtuple(t1, t2):
    '''
        >>> maxtuple((-4, 10, 8), (-100, 12, 19))
        (-4, 12, 19)
        >>> maxtuple((-4, 10), (-100, 12))
        (-4, 12)
    '''
    return tuple(max(x) for x in zip(t1, t2))

def mapvector(function, vector):
    return tuple(map(function, vector))

def directions(dimensions):
    '''
        Returns a list of vectors pointing in all cardinal demensinos for the given number
        >>> directions(1)
        [(1,), (-1,)]
    '''
    base=[0] * dimensions
    r=[]
    for x in range(dimensions):
       n = list(base)
       n[x] = 1
       r.append(tuple(n))
       n = list(base)
       n[x] = -1
       r.append(tuple(n))
    return r

def rotate2(vector, angle):
    '''
        Rotate a two dimensional vector clockwise.  UP is (0, -1), LEFT = (-1, 0)

        >>> rotate2((1, 0), -90)
        (0, -1)
        >>> rotate2((1, 0), 90)
        (0, 1)
        >>> rotate2((0, 1), -90)
        (1, 0)
        >>> rotate2((0, 1), 90)
        (-1, 0)
    '''
    c = int(math.cos(math.radians(angle)))
    s = int(math.sin(math.radians(angle)))
    return (vector[0] * c - vector[1] * s, vector[0] * s + vector[1] * c)

def rotate_matrix(matrix):
    '''
        Rotates the given two dimensional array (matrix) 90 clockwise.

        >>> [ ''.join(x) for x in rotate_matrix(['123', '456', '789', 'abc'])]
        ['a741', 'b852', 'c963']
        >>> [ ''.join(x) for x in rotate_matrix(['ab', 'cd'])]
        ['ca', 'db']
    '''
    result = []
    for x in range(len(matrix[0])):
         result.append([row[x] for row in reversed(matrix)])
    return result

def flip_matrix(matrix):
    '''
        Flips the given two dimensional array (matrix) along the x axis

        >>> [ ''.join(x) for x in flip_matrix(['123', '456', '789', 'abc'])]
        ['321', '654', '987', 'cba']
        >>> [ ''.join(x) for x in flip_matrix(['ab', 'cd'])]
        ['ba', 'dc']
    '''
    return [row[::-1] for row in matrix]

def minmax(*positions):
    '''
        Returns the minimum and maximum positions.
        The minimum position is a tuple containing the minimum of all positions.
        The maximym position is a tuple containing the maximym of all positions.
        >>> minmax((-4, 10), (4, -5))
        ((-4, -5), (4, 10))
        >>> minmax((-4, 10, 8), (4, -5, 5), (3, 1, 1), (-100, 10, 8))
        ((-100, -5, 1), (4, 10, 8))
        >>> minmax((-4, 10, 8))
        ((-4, 10, 8), (-4, 10, 8))
        >>> minmax(*zip(xrange(10), xrange(10)))
        ((0, 0), (9, 9))
    '''
    p2 = iter(itertools.tee(positions, 2))
    return (tuple(min(x) for x in zip(*p2.next())),
            tuple(max(x) for x in zip(*p2.next())))

def cubeintersect(p1, p2, s, radius):
    '''
        Returns true if the spehere (s, radius) intersects the cube defined by the points p1, p2
        >>> cubeintersect((0, 0, 0), (10, 10, 10), (5, 5, 5), 4)
        True
        >>> cubeintersect((0, 0, 0), (10, 10, 10), (5, 5, 5), 5)
        True
        >>> cubeintersect((0, 0, 0), (10, 10, 10), (-1, -1, -1), 2)
        True
        >>> cubeintersect((0, 0, 0), (10, 10, 10), (2, 2, 2), 1)
        True
        >>> cubeintersect((0, 0, 0), (10, 10, 10), (12, 12, 12), 1)
        False
        >>> cubeintersect((0, 0, 0), (10, 10, 10), (12, 12, 12), 3)
        False
        >>> cubeintersect((0, 0, 0), (10, 10, 10), (12, 12, 12), 3)
        False
        >>> cubeintersect((0, 0, 0), (10, 10, 10), (12, 12, 12), 3.5)
        True
        >>> cubeintersect((0, 0), (10, 10), (12, 12), 3)
        True
    '''
    squared = lambda sq: sq * sq
    dist_squared = squared(radius)
    minp, maxp = minmax(p1, p2)

    for x in range(len(minp)):
        if s[x] < minp[x]:
            dist_squared -= squared(s[x] - minp[x])
        elif s[0] > maxp[0]:
            dist_squared -= squared(s[x] - maxp[x])

    return dist_squared > 0

def min_gt(seq, val):
    """
    Return smallest item in seq for which item > val applies.
    None is returned if seq was empty or all items in seq were <= val.

    >>> min_gt([1, 3, 6, 7], 4)
    6
    >>> min_gt([2, 4, 7, 11], 5)
    7
    """

    for v in seq:
        if v > val:
            return v
    return None

def min_ge(seq, val):
    """
    Same as min_gt() except items equal to val are accepted as well.

    >>> min_ge([1, 3, 6, 7], 6)
    6
    >>> min_ge([2, 3, 4, 8], 8)
    8
    """

    for v in seq:
        if v >= val:
            return v
    return None

def max_lt(seq, val):
    """
    Return greatest item in seq for which item < val applies.
    None is returned if seq was empty or all items in seq were >= val.

    >>> max_lt([3, 6, 7, 11], 10)
    7
    >>> max_lt((5, 9, 12, 13), 12)
    9
    """

    idx = len(seq)-1
    while idx >= 0:
        if seq[idx] < val:
            return seq[idx]
        idx -= 1
    return None

def max_le(seq, val):
    """
    Same as max_lt(), but items in seq equal to val apply as well.

    >>> max_le([2, 3, 7, 11], 10)
    7
    >>> max_le((1, 3, 6, 11), 6)
    6
    """

    idx = len(seq)-1
    while idx >= 0:
        if seq[idx] <= val:
            return seq[idx]
        idx -= 1

    return None

def chunk(l, size):
    '''
        >>> list(chunk(range(21), 4))[1]
        [4, 5, 6, 7]
        >>> list(chunk(range(21), 5))[1]
        [5, 6, 7, 8, 9]
    '''
    for i in range(0, len(l), size):
        yield l[i:i + size]


class Thing:
    '''
         A generic object with attributes:
         t = Thing(a=5, b="hi")
         print(t.b)
         'hi'
    '''

    def __init__(self, **kwds):
        '''
            >>> t = Thing(name="name", value=2)
            >>> t.name
            'name'
            >>> t.value
            2
         '''
        self.__dict__.update(kwds)

class Repeat(object):
    '''
        Detect repeats
        r = Repeat()
        while not r.found:
            r.see(v)
        print(r)
    '''

    def __init__(self):
        self.seen =  {}
        self.cnt = 0
        self.found = False


    def see(self, val):
        if self.found:
            return
        if val in self.seen:
            self.start = self.seen[val]
            self.end = self.cnt
            self.val = val
            self.found = True
        self.seen[val] = self.cnt
        self.cnt += 1

    def __repr__(self):
        return "repeat(%d, %d)" % (self.start, self.end)


if __name__ == '__main__':
    import doctest
    doctest.testmod()
