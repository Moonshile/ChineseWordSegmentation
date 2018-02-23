#coding=utf-8

"""
A simple frequent itemset mining algorithm implementation
Author: 段凯强
"""

import itertools

from wordseg.sequence import dedup
from wordseg.hashtree import HashTree, sameNodes
from functools import reduce

class FreqItem(object):
    def __init__(self, transactions, sup_theta=.1):
        self.transactions = [sorted(t) for t in [x for x in transactions if x]]
        self.sup_theta = sup_theta*len(transactions)
        self.freqset = []

    def filterCandidates(self, cand):
        """
        Build a HashTree with candidates cand, then count support of these candidates to filter out
        all those that have support not lower than sup_theta
        """
        hashtree = HashTree(cand)
        hashtree.count(self.transactions)
        return hashtree.getNodes(self.sup_theta)

    def freqOneSet(self):
        """
        Generate frequent 1-item sets
        """
        one_item_cand = set()
        for t in self.transactions:
            for w in t:
                one_item_cand.add(w)
        return sorted(self.filterCandidates([[i] for i in one_item_cand]), key=lambda i: i[0].name)

    def genNextCand(self, preItems):
        """
        Generate next candidates by dynamic programming
        Find range [i, j) such that items in this range have same prefix
        e.g., [1,2,3,4] and [1,2,3,5] have same prefix, so they should be in one same range
        Then, generate 2-combinations of these ranges as result
        """
        res = []
        i, j = 0, 0
        while i < len(preItems):
            if j < len(preItems) and sameNodes(preItems[j][:-1], preItems[i][:-1]):
                j += 1
            else:
                res += [pair[0] + [pair[1][-1]] for pair in itertools.combinations(preItems[i:j], 2)]
                i = j
        return [[i.name for i in items] for items in res]

    def genFreqItemSets(self):
        """
        @return Frequent item sets with their frequency
        """
        if self.freqset: return self.freqset
        cur = self.freqOneSet()
        freqKSet = []
        while cur:
            freqKSet.append(cur)
            cur = self.filterCandidates(self.genNextCand(cur))
        self.freqset = reduce(lambda res, x: res + x, freqKSet, [])
        name_freq_pairs = [[(i.name, i.val) for i in items] for items in self.freqset[::-1]]
        res = [list(zip(*items)) for items in name_freq_pairs]
        return [(list(pair[0]), pair[1][-1]) for pair in res]

if __name__ == '__main__':
    transactions = [[1,2,3],[1,2,4],[2,4,6,8],[1,3,5,7], [5,7,2]]
    freqItem = FreqItem(transactions, sup_theta=.3)
    print(freqItem.genFreqItemSets())
