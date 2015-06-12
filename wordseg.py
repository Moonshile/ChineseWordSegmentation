#coding=utf-8

"""
Chinese word segmentation algorithm without corpus
Author: 段凯强
Reference: http://www.matrix67.com/blog/archives/5044
"""

import re

from probability import entropyOfList
from sequence import genSubparts




def indexOfSortedSuffix(doc, max_word_len):
    indexes = []
    length = len(doc)
    for i in xrange(0, length):
        for j in xrange(i + 1, min(i + 1 + max_word_len, length + 1)):
            indexes.append((i, j))
    return sorted(indexes, key=lambda (i, j): doc[i:j])


class WordInfo(object):
    """
    Store information of each word, including its freqency, left neighbors and right neighbors
    """
    def __init__(self, text):
        super(WordInfo, self).__init__()
        self.text = text
        self.freq = 0
        self.left = []
        self.right = []

    def update(self, left, right):
        self.freq += 1
        if left: self.left.append(left)
        if right: self.right.append(right)

    def compute(self, length):
        self.p = self.freq/float(length)
        self.left = entropyOfList(self.left)
        self.right = entropyOfList(self.right)

    def computeAggregation(self, words_dict):
        self.aggregation = 0
        parts = genSubparts(self.text)
        if len(parts) > 0:
            self.aggregation = min(map(
                lambda (p1, p2): self.p/words_dict[p1].p/words_dict[p2].p,
                parts
            ))



def wordSegment(doc, max_word_len=5, min_freq=2, min_entropy=2.0, min_aggregation=50):
    pattern = re.compile(u'[\s,.<>/?:;\'\"[\\]{}()\\|~!@#$%^&*-_=+a-zA-Z，。《》、？：；“‘｛｝【】（）…￥！—]+')
    doc = re.sub(pattern, '', doc)
    suffix_indexes = indexOfSortedSuffix(doc, max_word_len)
    word_cands = {}
    # compute frequency and neighbors
    for suf in suffix_indexes:
        word = doc[suf[0]:suf[1]]
        if word not in word_cands:
            word_cands[word] = WordInfo(word)
        word_cands[word].update(doc[suf[0] - 1:suf[0]], doc[suf[1]:suf[1] + 1])
    # compute probability and entropy
    length = len(doc)
    for k in word_cands:
        word_cands[k].compute(length)
    # compute aggregation of words whose length > 1
    values = sorted(word_cands.values(), key=lambda x: len(x.text))
    for v in values:
        if len(v.text) == 1: continue
        v.computeAggregation(word_cands)
    # words which satisfies the conditions
    sat_words = {}
    for v in values:
        if len(v.text) > 1 and v.aggregation > min_aggregation and\
                v.freq > min_freq and v.left > min_entropy and v.right > min_entropy:
            sat_words[v.text] = v
    # remove long words that are combinations of shorter words
    res = []
    for v in sat_words.values():
        if len(v.text) == 2:
            res.append(v)
            continue
        if reduce(lambda res, (p1, p2): res or p1 in sat_words and p2 in sat_words, genSubparts(v.text), False):
            continue
        res.append(v)
    return map(lambda x: x.text, sorted(res, key=lambda v: v.freq, reverse=True))








