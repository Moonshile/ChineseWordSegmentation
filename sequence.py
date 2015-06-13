#coding=utf-8

def genSubstr(string, n):
    """
    Generate all substrings of max length n for string
    """
    length = len(string)
    res = []
    for i in range(0, length):
        for j in range(i + 1, min(i + n + 1, length + 1)):
            res.append(string[i: j])
    return res

def genSubparts(string):
    """
    Partition a string into all possible two parts, e.g.
    given "abcd", generate [("a", "bcd"), ("ab", "cd"), ("abc", "d")]
    For string of length 1, return empty list
    """
    length = len(string)
    res = []
    for i in range(1, length):
        res.append((string[0:i], string[i:]))
    return res

