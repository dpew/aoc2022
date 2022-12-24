#!/usr/bin/env python3

import numpy as np
import math

mt = [[1, 0, 0, 0],
      [0, 1, 0, 0],
      [0, 0, 1, 0],
      [0, -4, 0, 1]]

mr = [[0, 0, 1, 0],
      [0, 1, 0, 0],
      [-1, 0, 0, 0],
      [0, 0, 0, 1]]

def translate(dx: int, dy: int, dz: int):
    return [
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [dx, dy, dz, 1]]

def rotateX(deg: int):
    rad = deg * math.pi / 180.0
    cval = int(math.cos(rad))    
    sval = int(math.sin(rad))
#     print(f"deg={deg} cos={cval} sin={sval}")
    return  [
      [    1,    0,     0, 0],
      [    0, cval, -sval, 0],
      [    0, sval,  cval, 0],
      [    0,    0,     0, 1]]

def rotateY(deg: int):
    rad = deg * math.pi / 180.0
    cval = int(math.cos(rad))
    sval = int(math.sin(rad))
    return  [
      [ cval,    0, sval, 0],
      [    0,    1,    0, 0],
      [ -sval,   0, cval, 0],
      [    0,    0,    0, 1]]

def rotateZ(deg: int):
    rad = deg * math.pi / 180.0
    cval = int(math.cos(rad))
    sval = int(math.sin(rad))
    return  [
      [ cval, -sval, 0, 0],
      [ sval, cval, 0, 0],
      [    0,    0, 1, 0],
      [    0,    0, 0, 1]]

def mkpos(x: int, y: int, z: int):
    return (x, y, z, 1)

def dot(x, y, desc=None):
    if not desc:
        desc = str(y)
    r = list(np.dot(x, y))
    print(f"{desc}: {x} -> {r}")

pos=mkpos(3, 4, 5)
dot(pos, rotateX(90), "rotX(90) ")
dot(pos, rotateX(180), "rotX(180)")
dot(pos, rotateX(270), "rotX(270)")
dot(pos, rotateX(360), "rotX(360)")
print()
dot(pos, rotateY(90),  "rotY(90) ")
dot(pos, rotateY(180), "rotY(180)")
dot(pos, rotateY(270), "rotY(270)")
dot(pos, rotateY(360), "rotY(360)")
print()
dot(pos, rotateZ(90),  "rotZ(90) ")
dot(pos, rotateZ(180), "rotZ(180)")
dot(pos, rotateZ(270), "rotZ(270)")
dot(pos, rotateZ(360), "rotZ(360)")
# print(np.dot(pos, mr))
# print(np.dot(pos, mtr))


