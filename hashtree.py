#coding=utf-8

"""
A simple implementation of Hash Tree
Author: 段凯强
"""

class HashTreeNode(object):
    def __init__(self, name=''):
        self.val = 0
        self.name = name
        self.level = 0
        self.children = {}

    def addBag(self, bag):
        """
        Note that bag must be sorted
        """
        if bag:
            node = self.children.get(bag[0], HashTreeNode(name=bag[0]))
            node.addBag(bag[1:])
            self.children[bag[0]] = node
            self.level = len(bag)

    def count(self, transaction):
        """
        count the child who matches bag, suppose that current node matches
        """
        if self.level == 0:
            self.val += 1
        elif self.level == 1:
            for t in transaction:
                if t in self.children: self.children[t].val += 1
        else:
            for i in range(0, len(transaction)):
                t = transaction[i]
                if t in self.children:
                    self.children[t].count(transaction[i:])

    def get(self, theta):
        if self.level == 0:
            return [[self.name]] if self.val >= theta else None
        else:
            children_res = [self.children[i].get(theta) for i in sorted(self.children.keys())]
            total = reduce(lambda res, x: res + x, filter(lambda x: x, children_res), [])
            return map(lambda c: [self.name] + c, total)

    def __str__(self):
        return '(%s : %s)'%(self.name, '; '.join([str(i) for i in self.children.values()]))


class HashTree(object):
    """
    Note that all bags must be sorted
    """
    def __init__(self, bags):
        self.root = HashTreeNode()
        self.root.val = 0
        for b in bags:
            if b: self.root.addBag(b)

    def count(self, transactions):
        for t in transactions: self.root.count(t)

    def get(self, theta):
        res = map(lambda c: c[1:], self.root.get(theta))
        return [] if res == [[]] else res

    def __str__(self):
        return str(self.root)

if __name__ == '__main__':
    to_count = [[1,2], [2,4], [1,3], [1,5], [3,4], [2,7], [6,8]]
    tree = HashTree(to_count)
    transactions = [[1,2,3],[1,2,4],[2,4,6,8],[1,3,5,7]]
    tree.count(transactions)
    print 'Frequency with transactions', transactions
    print tree.get(2)
    print tree.get(1)


