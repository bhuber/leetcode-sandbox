from unittest import TestCase

from graphs import ComponentSets


class TestComponentSets(TestCase):
    undertest = ComponentSets()
    def test_basic(self):
        self.undertest.add(1)
        self.undertest.add(2)
        self.assertEqual(1, self.undertest.representative(1))
        self.assertEqual(2, self.undertest.representative(2))

        self.undertest.union(1, 2)
        self.assertEqual(self.undertest.representative(1), self.undertest.representative(2))

    def test_union(self):
        for i in range(0, 10):
            self.undertest.add(i)

        for i in range(0, 10):
            self.assertEqual(i, self.undertest.representative(i))

        for i in range(1, 10):
            self.undertest.union(1, i)

        distinct_components = set(self.undertest.representative(i) for i in range(1, 10))
        self.assertEqual(1, len(distinct_components))

    def test_union_2(self):
        for i in range(0, 10):
            self.undertest.add(i)

        for i in range(1, 4):
            self.undertest.union(0, i)
        for i in range(5, 7):
            self.undertest.union(4, i)
        self.undertest.union(7, 8)

        distinct_components = set(self.undertest.representative(i) for i in range(1, 10))
        self.assertEqual(4, len(distinct_components))

        self.undertest.union(3, 4)
        self.undertest.union(9, 8)
        self.undertest.union(7, 5)

        distinct_components = set(self.undertest.representative(i) for i in range(1, 10))
        self.assertEqual(1, len(distinct_components))
