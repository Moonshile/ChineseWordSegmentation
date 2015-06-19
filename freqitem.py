#coding=utf-8

"""
A simple frequent itemset mining algorithm implementation
Author: 段凯强
"""

import itertools

from sequence import dedup
from hashtree import HashTree

class FreqItem(object):
    def __init__(self, transactions, sup_theta=.1):
        self.transactions = [sorted(t) for t in filter(lambda x: x, transactions)]
        self.sup_theta = sup_theta*len(transactions)
        self.freqset = []

    def filterCandidates(self, cand):
        hashtree = HashTree(cand)
        hashtree.count(self.transactions)
        return hashtree.get(self.sup_theta)

    def freqOneSet(self):
        """
        Generate frequent 1-item sets
        """
        one_item_cand = set()
        for t in self.transactions:
            for w in t:
                one_item_cand.add(w)
        return sorted(self.filterCandidates([[i] for i in one_item_cand]))

    def genNextCand(self, preItems):
        res = []
        # Generate next candidates by dynamic programming
        i, j = 0, 0
        while i < len(preItems):
            if j < len(preItems) and preItems[j][:-1] == preItems[i][:-1]:
                j += 1
            else:
                res += [pair[0] + [pair[1][-1]] for pair in itertools.combinations(preItems[i:j], 2)]
                i = j
        return res

    def genFreqItemSets(self):
        if self.freqset: return self.freqset
        cur = self.freqOneSet()
        freqKSet = []
        while cur:
            freqKSet.append(cur)
            cur = self.filterCandidates(self.genNextCand(cur))
        self.freqset = reduce(lambda res, x: res + x, freqKSet, [])
        return self.freqset[::-1]



if __name__ == '__main__':
    transactions = [[1,2,3],[1,2,4],[2,4,6,8],[1,3,5,7], [5,7,2]]
    freqItem = FreqItem(transactions, sup_theta=.3)
    print freqItem.genFreqItemSets()
