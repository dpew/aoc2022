#!/usr/bin/env python
from __future__ import print_function

import sys
import math
import pprint
import os
import re
import doctest
import itertools
import types
import logging
from collections import deque
from collections import defaultdict

# create absolute mydir
mydir = os.path.abspath(os.path.dirname(__file__))
sys.path.append(os.path.join(mydir, '../lib'))

from advent import *

class Promise(object):

    def __init__(self, resolve):
        self._resolve = resolve
        self._value = None
        self._resolved = False

    def resolve(self, value):
        if not self._resolved:
            self._resolved = True
            self._value = value
            self._resolve(value)
        return self._value

    @property
    def completed(self):
        return self._resolved

    @property
    def value(self):
        return self._value

class bcolors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def decode_opcode(opcode):
    '''
       Returns opcode, param1, param2, param3
       ABCDE
        1002

       DE - two-digit opcode,      02 == opcode 2
       C - mode of 1st parameter,  0 == position mode
       B - mode of 2nd parameter,  1 == immediate mode
       A - mode of 3rd parameter,  0 == position mode,
                                  omitted due to being a leading zero
       >>> decode_opcode(1002)
       (2, (0, 1, 0))
       >>> decode_opcode(71315)
       (15, (3, 1, 7))
    '''
    fopcode = '00000' + str(opcode)
    parms = fopcode[-3], fopcode[-4], fopcode[-5]
    return int(fopcode[-2:]), tuple(int(p) for p in parms)

def getparms(pos, memory, *pmode, **kw):
    '''
        Returns the parameters from memory
        getparms(memory, pmode1, pmode2, ...)

        pmode:
            0 = position mode
            1 = immediate mode

        >>> getparms(1, [1002, 4, 3, 4, 33], 0, 1, 1)
        (33, 3, 4)
        >>> getparms(2, [1002, 4, 4, 2, 5, 1024], 1, 1, 0)
        (4, 2, 1024)
        >>> getparms(3, [3, 225, 1, 1, 6, 6, 450], 0, 0, 1)
        (225, 450, 6)
        >>> getparms(1, [1002, 4, 3, 4, 33], 0, 1, 2, relpos=0)
        (33, 3, 33)
        >>> getparms(1, [1002, 4, 3, 4, 33], 0, 1, 2, relpos=-1)
        (33, 3, 4)
    '''
    logger = logging.getLogger("getparms")
    params=[]
    paramdebug=[]
    relpos = kw.get("relpos", "ERROR")
    #logger.debug("getparms(%d, %s, %s) relpos=%d:", pos, memory[pos:pos+len(pmode)], pmode, relpos)
    for e, p in enumerate(pmode):
        try:
            param = memory[pos + e]
            pdebug = "%d=m[%d + %d]" % (param, pos, e)
        except IndexError:
            pdebug = "%d=INDEXERR(m[%d + %d])" % (param, pos, e)
            #print("getparms[memory[%d + %d]]: IndexError.  Out of range[0:%d]" % (pos, e, len(memory)))
            #print(printmem(memory, pos))
            #raise
            param = 0
        if p in (0, 2):
           try:
               param = memory[param + (relpos if p == 2 else 0)]
               pdebug = "%d=m[%s + %s]" % (param, pdebug, str(relpos) if p == 2 else "0")
           except IndexError:
               #print("getparms[memory[param=%d]: IndexError.  Out of range[0:%d], relpos=%d" % (param, len(memory), relpos))
               #print(printmem(memory, pos))
               #raise
               param = 0
               pdebug = "%d=INDEXERR(m[%s%s])" % (param, pdebug, "+%d"%(relpos,) if p == 2 else "")
        params.append(param)
        paramdebug.append(pdebug)
    logger.debug("getparms(%d, %s, %s, relpos=%s): %s" % (pos, memory[pos:pos+len(pmode)], pmode, relpos, params))
    logger.debug(", ".join(paramdebug))

    return tuple(params)

class Memory(object):

    def __init__(self, *args, **kw):
        self.data = list(*args)

    def reset(self, memory):
        self.data = list(memory)

    def write(self, pos, val):
        '''
            >>> Memory([1, 2, 3]).write(5, 1000)
            [1, 2, 3, 0, 0, 1000]
            >>> Memory([1, 2, 3]).write(3, 4)
            [1, 2, 3, 4]
            >>> Memory([1, 2, 3]).write(1, 8)
            [1, 8, 3]
        '''
        #if relmode in (0, 2):
        #    logging.warn("Writing relative mode at position %s, value %d" % (pos, val))
        #    pos = self[pos] + (relpos if relmode == 2 else 0)
        if pos >= len(self.data):
            self.data.extend([0] * (1 + pos - len(self.data)))
        self.data[pos] = val
        return self

    def read(self, pos):
        return 0 if pos >= len(self.data) else self.data[pos]

    def printitem(self, pos, item, meminfo):
        color = ''
        if pos == meminfo.pos:
           color = color + bcolors.RED + bcolors.UNDERLINE
        return '{} {:6d}{}'.format(color, item, bcolors.ENDC)

    def printmem(self, meminfo=Thing(pos=-1), width=20):
        cstr=[]
        for ce, c in enumerate(chunk(self.data, width)):
           cstr.append("%3d:"%(ce * width) +
              "".join(self.printitem(ce * width + e, x, meminfo) for e, x in enumerate(c)))
        return "\n ".join(cstr)

    def __repr__(self):
        return repr(self.data)

class Opcode(object):

    '''
        >>> Opcode(1, argcount=2, output=True, func=lambda c, x, y: x+y, name='ADD')
        ADD(param1, param2, oparam)
        >>> Opcode(2, argcount=0, output=True, func=lambda c, x, y: x+y, name='INPUT')
        INPUT(oparam)
        >>> Opcode(3)
        OPCODE03()
    '''
    def __init__(self, opcode, **kw):
        self.opcode = opcode
        self.argcount = kw.get('argcount', 0)
        self.oflag = kw.get('output', False)
        self.apply = kw.get('func', )
        self.name = kw.get('name', "OPCODE{:02d}".format(self.opcode))
        self.step = self.argcount + (1 if self.oflag else 0)

    def __repr__(self):
        args=["param{:d}".format(x+1) for x in xrange(self.argcount)]
        if self.oflag:
            args.append("oparam")
        return "{:s}({:s})".format(self.name, ", ".join(args))

class Computer(object):

    OPCODES = [
        Opcode(1, name='ADD', argcount=2, output=True, func=lambda c, p1, p2: p1+p2),
        Opcode(2, name='MUL', argcount=2, output=True, func=lambda c, p1, p2: p1*p2),
        Opcode(3, name='IN', output=True, func=lambda c: c.input() ),
        Opcode(4, name='OUT', argcount=1, func=lambda c, p1: c.output(p1) ),
        Opcode(5, name='JYS', argcount=2, func=lambda c, p1, p2: c.jumpif(p1 != 0, p2)),
        Opcode(6, name='JNO', argcount=2, func=lambda c, p1, p2: c.jumpif(p1 == 0, p2)),
        Opcode(7, name='LT', argcount=2, output=True, func=lambda c, p1, p2: 1 if p1 < p2 else 0),
        Opcode(8, name='EQ', argcount=2, output=True, func=lambda c, p1, p2: 1 if p1 == p2 else 0),
        Opcode(9, name='REL', argcount=1, func=lambda c, p1: c.addrelpos(p1)),
        Opcode(99, name='HLT', func=lambda c: c.halt())
    ]

    OPCODEMAP = dict((op.opcode, op) for op in OPCODES)

    def __init__(self, memory, inputter, outputter):
        self.logger = logging.getLogger("intcode")
        self.pos = 0
        self.relpos = 0
        self.memory = memory
        self.inputter = inputter
        self.outputter = outputter

    def input(self):
        return self.inputter()

    def output(self, value):
        return self.outputter(value)

    def jumpif(self, flag, newpos):
        if (flag):
            self.logger.info("POS=%d", newpos)
            self.pos = newpos

    def halt(self):
        self.pos = -1

    def reset(self):
        self.pos = 0
        self.relpos = 0

    def addrelpos(self, relpos):
        self.relpos += relpos

    @property
    def halted(self):
        return self.pos < 0

    def _read_mem(self, pos, pmode):
        '''
             Read memory based on pmode
             Returns (memval, pos, debug)
        '''
        memval = self.memory.read(pos)
        #debug = "M[{:d}]={:d}".format(pos, memval)
        debug = "{:d}".format(memval)
        if pmode == 0: # position mode
            pos = memval
            memval = self.memory.read(pos)
            debug="M[{:s}]={:d}".format(debug, memval)
        elif pmode == 2: # relative mode
            pos = memval + self.relpos
            memval = self.memory.read(pos)
            debug="M[R[{:d}] + {:s}]={:d}".format(self.relpos, debug, memval)
        return (memval, pos, debug)

    def _read_params(self, argcount, pmode):
        return [ self._read_mem(self.pos + 1 + i, pmode[i]) for i in xrange(argcount) ]

    def async_step(self):
        if self.pos < 0:
            raise StopIteration()

        # Decode operand
        opcode, pmode = decode_opcode(self.memory.read(self.pos))
        try:
            operand = Computer.OPCODEMAP[opcode]
        except KeyError:
            self.logger.error('%d: Bad opcode %d', self.pos, opcode)
            raise

        parameters = self._read_params(operand.argcount, pmode)

        # Get the actual values from parameters and make debug statement
        pvals = [p[0] for p in parameters]
        pdebug = [ "P{:d}={:s}".format(e+1, p[2]) for e, p in enumerate(parameters) ]
        debug = "[{:3d}: {:s}] {:s} {:s}".format(self.pos,
                                    " ".join(str(i) for i in self.memory.data[self.pos:self.pos + 1 + operand.step]),
                                    operand.name,
                                    " ".join(str(i) for i in pvals))

        lastpos = self.pos
        self.pos += 1 + operand.step

        result = yield operand.apply(self, *pvals)
        if operand.oflag:
            rflag = pmode[operand.argcount] == 2
            rpos = 0
            rdebug = ""
            if rflag:
                rpos = self.relpos
                rdebug = "R{:d} + ".format(rpos)
            writepos = self.memory.read(lastpos + 1 + operand.argcount)
            self.memory.write(writepos + rpos, result)
            pdebug.insert(0, "M[{:s}{:d}]:={:d}".format(rdebug, writepos, result))
        self.logger.info("%s %s", debug, ", ".join(pdebug))

    def step(self):
        '''
            Runs one step in the computer
        '''
        gen = self.async_step()
        try:
            lastval = gen.next()
            gen.send(lastval)
        except StopIteration:
            pass

    def execute(self):
        '''
            A generator that runs until input yielded
        '''
        lastval = None
        while self.pos >= 0:
            gen = self.async_step()
            try:
                lastval = gen.next()
                if isinstance(lastval, Promise):
                    lastval = yield lastval
                lastval = gen.send(lastval)
            except StopIteration:
                pass
        else:
            raise StopIteration()

    def run(self):
        '''
            Run continuously
        '''
        lastval = None
        while True:
            try:
                gen = self.execute()
                lastval = gen.send(lastval)
            except StopIteration:
                logging.debug("STOP")
                return



if __name__ == '__main__':
    import doctest
    doctest.testmod()

    logging.basicConfig(level=logging.DEBUG)

    # Some computer tests
    c = Computer(Memory([1, 2, 3, 10, 4, 10, 99]), lambda: 0, lambda p1: print("OUTPUT {:d}".format(p1)))
    c.run()
    sys.exit(0)
