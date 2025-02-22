from collections import defaultdict
from itertools import chain
from numbers import Number
from typing import Any, Tuple, List

class Node:
    def __init__(self, id: Any, data: Any = None, edges: List[Tuple[Any, Number]] = None):
        self.id = id
        self.data = data
        self.edges = edges if edges else []

class ComponentSets:
    def __init__(self):
        self.rank = defaultdict(lambda: 0)
        self.parents = {}

    def add(self, e):
        self.rank[e] = 1
        self.parents[e] = e

    def representative(self, e):
        maybe_result = self.parents[e]
        if maybe_result == e:
            return maybe_result
        else:
            result = self.representative(maybe_result)
            self.parents[e] = result
            return result

    def union(self, e1, e2):
        re1 = self.representative(e1)
        re2 = self.representative(e2)
        if self.rank[re1] >= self.rank[re2]:
            self.parents[re2] = re1
            self.rank[re1] += self.rank[re2]
        else:
            self.parents[re1] = re2
            self.rank[re2] += self.rank[re1]


class UndirectedGraph:
    def __init__(self, edgelist: List[Tuple[Any, Any, Number]]):
        self.edgelist = edgelist
        self.nodes = set(chain((e[0] for e in edgelist), (e[1] for e in edgelist)))

    def __getitem__(self, key):
        if key not in self.nodes:
            raise KeyError(f"Node {key} not found in graph.")
        return Node(key, edges=[(e[1], e[2]) for e in self.edgelist if e[0] == key])

    def __repr__(self):
        return f"UndirectedGraph({self.edgelist})"

    def __str__(self):
        return self.__repr__()

    def kruskal(self, start):
        pass