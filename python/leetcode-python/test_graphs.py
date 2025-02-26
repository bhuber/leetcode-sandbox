from unittest import TestCase

from graphs import ComponentSets, Graph


def udg_1():
    return [
        ('a', 'b', 4),
        ('a', 'h', 8),
        ('b', 'c', 8),
        ('b', 'h', 11),
        ('c', 'i', 2),
        ('c', 'f', 4),
        ('c', 'd', 7),
        ('d', 'e', 9),
        ('d', 'f', 14),
        ('e', 'f', 10),
        ('f', 'g', 2),
        ('g', 'i', 6),
        ('g', 'h', 1),
        ('h', 'i', 7),
    ]


def dg_1():
    return [(x[0], x[1], 1) for x in [
        ('a', 'b'),
        ('b', 'c'),
        ('b', 'e'),
        ('b', 'f'),
        ('c', 'd'),
        ('c', 'g'),
        ('d', 'c'),
        ('d', 'h'),
        ('e', 'a'),
        ('e', 'f'),
        ('f', 'g'),
        ('g', 'f'),
        ('g', 'h'),
        ('h', 'h'),
    ]]


def dg_2():
    return [(x[0], x[1], 1) for x in [
        ('a', 'b'),
        ('b', 'e'),
        ('c', 'd'),
        ('d', 'c'),
        ('e', 'a'),
        ('f', 'g'),
        ('g', 'f'),
        ('h', 'h'),
    ]]


class TestComponentSets(TestCase):
    ut = ComponentSets()

    def test_basic(self):
        self.ut.add(1)
        self.ut.add(2)
        self.assertEqual(1, self.ut.representative(1))
        self.assertEqual(2, self.ut.representative(2))

        self.ut.union(1, 2)
        self.assertEqual(self.ut.representative(1), self.ut.representative(2))

    def test_union(self):
        for i in range(0, 10):
            self.ut.add(i)

        for i in range(0, 10):
            self.assertEqual(i, self.ut.representative(i))

        for i in range(1, 10):
            self.ut.union(1, i)

        distinct_components = set(self.ut.representative(i) for i in range(1, 10))
        self.assertEqual(1, len(distinct_components))

    def test_union_2(self):
        for i in range(0, 10):
            self.ut.add(i)

        for i in range(1, 4):
            self.ut.union(0, i)
        for i in range(5, 7):
            self.ut.union(4, i)
        self.ut.union(7, 8)

        distinct_components = set(self.ut.representative(i) for i in range(1, 10))
        self.assertEqual(4, len(distinct_components))

        self.ut.union(3, 4)
        self.ut.union(9, 8)
        self.ut.union(7, 5)

        distinct_components = set(self.ut.representative(i) for i in range(1, 10))
        self.assertEqual(1, len(distinct_components))


class TestGraphs(TestCase):
    def test_dfs1(self):
        ut = Graph(udg_1(), False)
        dfs = ut.dfs()
        print(dfs)
        self.assertEqual(1, len(dfs))
        self.assertEqual(9, len(set(dfs[0])))

    def test_dfs2(self):
        ut = Graph(dg_1(), True)
        dfs = ut.dfs()
        print(dfs)
        self.assertEqual(1, len(dfs))
        self.assertEqual(8, len(set(dfs[0])))

    def test_dfs3(self):
        ut = Graph(dg_2(), True)
        dfs = ut.dfs()
        print(dfs)
        expected = sorted(sorted(sc) for sc in [['a', 'b', 'e'], ['f', 'g'], ['d', 'c'], ['h']])
        self.assertEqual(4, len(dfs))
        self.assertEqual(expected, sorted(sorted(tree) for tree in dfs))

    def test_kruskal(self):
        ut = Graph(udg_1(), False)
        mst = ut.kruskal()

        print(mst)
        self.assertEqual(8, len(mst))

        expected_mst_check = {
            'min_mst_weight': 33,
            'spanned_nodes': ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i'],
            'n_spanned_nodes': 9,
            'is_full_span': True,
            'mst_weight': 37}
        self.assertEqual(expected_mst_check, ut.check_mst(mst))

    def test_prim(self):
        ut = Graph(udg_1(), False)
        mst = ut.prim('a')

        print(mst)
        self.assertEqual(8, len(mst))

        expected_mst_check = {
            'min_mst_weight': 33,
            'spanned_nodes': ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i'],
            'n_spanned_nodes': 9,
            'is_full_span': True,
            'mst_weight': 37}
        self.assertEqual(expected_mst_check, ut.check_mst(mst))
