#coding=utf-8

import math

def entropyOfList(ls):
    elements = {}
    for e in ls:
        elements[e] = elements.get(e, 0) + 1
    length = float(len(ls))
    return sum(map(lambda v: -v/length*math.log(v/length), elements.values()))
        


