#coding=utf-8

"""
Algorithms about probability
Author: 段凯强
"""

import math

def entropyOfList(ls):
    """
    Given a list of some items, compute entropy of the list
    The entropy is sum of -p[i]*log(p[i]) for every unique element i in the list, and p[i] is its frequency
    """
    elements = {}
    for e in ls:
        elements[e] = elements.get(e, 0) + 1
    length = float(len(ls))
    # if length is 0, which means one side of a work is empty, which is only one single determinated case, so entropy should be 0
    return length and sum([-v/length*math.log(v/length) for v in list(elements.values())])



