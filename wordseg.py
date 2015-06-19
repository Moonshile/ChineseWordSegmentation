#coding=utf-8

"""
Chinese word segmentation algorithm without corpus
Author: 段凯强
Reference: http://www.matrix67.com/blog/archives/5044
"""

import re

from probability import entropyOfList
from sequence import genSubparts, genSubstr




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
        self.freq = 0.0
        self.left = []
        self.right = []

    def update(self, left, right):
        self.freq += 1
        if left: self.left.append(left)
        if right: self.right.append(right)

    def compute(self, length):
        self.freq /= length
        self.left = entropyOfList(self.left)
        self.right = entropyOfList(self.right)

    def computeAggregation(self, words_dict):
        self.aggregation = 0
        parts = genSubparts(self.text)
        if len(parts) > 0:
            self.aggregation = min(map(
                lambda (p1, p2): self.freq/words_dict[p1].freq/words_dict[p2].freq,
                parts
            ))



class WordSegment(object):

    """
    Main class for Chinese word segmentation
    1. Generate words from a long enough document
    2. Do the segmentation work with the document
    """

    # if a word is combination of other shorter words, then treat it as a long word
    L = 0
    # if a word is combination of other shorter words, then treat it as the set of shortest words
    S = 1
    # if a word contains other shorter words, then return all possible results
    ALL = 2

    def __init__(self, doc, max_word_len=5, min_freq=0.00005, min_entropy=2.0, min_aggregation=50):
        super(WordSegment, self).__init__()
        self.max_word_len = max_word_len
        self.min_freq = min_freq
        self.min_entropy = min_entropy
        self.min_aggregation = min_aggregation
        self.words = self.genWords(doc)

    def genWords(self, doc):
        pattern = re.compile(u'[\\s\\d,.<>/?:;\'\"[\\]{}()\\|~!@#$%^&*\\-_=+a-zA-Z，。《》、？：；“”‘’｛｝【】（）…￥！—┄－]+')
        doc = re.sub(pattern, '', doc)
        suffix_indexes = indexOfSortedSuffix(doc, self.max_word_len)
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
            if len(v.text) > 1 and v.aggregation > self.min_aggregation and\
                    v.freq > self.min_freq and v.left > self.min_entropy and v.right > self.min_entropy:
                sat_words[v.text] = v
        return set(map(lambda x: x.text, sorted(sat_words.values(), key=lambda v: v.freq, reverse=True)))

    def segSentence(self, sentence, method=ALL):
        i = 0
        res = []
        while i < len(sentence):
            if method == self.L or method == self.S:
                j_range = range(self.max_word_len, 0, -1) if method == self.L else range(2, self.max_word_len + 1) + [1]
                for j in j_range:
                    if j == 1 or sentence[i:i + j] in self.words:
                        res.append(sentence[i:i + j])
                        i += j
                        break
            else:
                to_inc = 1
                for j in range(2, self.max_word_len + 1):
                    if i + j <= len(sentence) and sentence[i:i + j] in self.words:
                        res.append(sentence[i:i + j])
                        if to_inc == 1: to_inc = j
                if to_inc == 1: res.append(sentence[i])
                i += to_inc
        return res






