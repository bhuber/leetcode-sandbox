import functools
import heapq
import itertools
from collections import defaultdict
from functools import cache
from itertools import chain
from numbers import Number
from typing import Any, Tuple, List, Iterable


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

class Colors:
    WHITE = "WHITE"
    GRAY = "GRAY"
    BLACK = "BLACK"

def flatten(list_of_lists):
    return list(itertools.chain.from_iterable(list_of_lists))

@functools.total_ordering
class Edge[T]:
    def __init__(self, start: T, end: T, weight: Number):
        self.start = start
        self.end = end
        self.weight = weight

    def __lt__(self, other):
        return isinstance(other, Edge) and self.weight < other.weight

    def __eq__(self, other):
        return isinstance(other, Edge) and (
            self.start == other.start and
            self.end == other.end and
            self.weight == other.weight)


    def __repr__(self):
        return f"Edge: {self.start}->{self.end}, {self.weight}"

    def __str__(self):
        return self.__repr__()


class Graph[T]:
    def __init__(self, edgelist: Iterable [Tuple[T, T, Number]], directed=True):
        self.directed = directed
        """
        self.edgelist: List[Edge] = sorted(Edge(e[0], e[1], e[2]) for e in (
            set(edgelist)
            if directed else
            set(chain(edgelist, ((e[1], e[0], e[2]) for e in edgelist)))))
        """
        self.edgelist: List[Edge] = sorted(Edge(e[0], e[1], e[2]) for e in (set(edgelist)))
        self.nodes = set(chain((e[0] for e in edgelist), (e[1] for e in edgelist)))

    def __getitem__(self, key: T):
        if key not in self.nodes:
            raise KeyError(f"Node {key} not found in graph.")
        return Node(key, edges=[(e[1], e[2]) for e in self.edgelist if e[0] == key])

    @cache
    def neighbors(self, n: T) -> List[T]:
        result = [e.end for e in self.edgelist if e.start == n]
        if not self.directed:
            result += [e.start for e in self.edgelist if e.end == n]
        return result

    @cache
    def out_edges(self, n: T) -> List[Edge[T]]:
        result = [e for e in self.edgelist if e.start == n]
        if not self.directed:
            result += [Edge(e.end, e.start, e.weight) for e in self.edgelist if e.end == n]
        return result


    def __repr__(self):
        return ("DirectedGraph" if self.directed else "UndirectedGraph") + f"({self.edgelist})"

    def __str__(self):
        return self.__repr__()

    def dfs(self) -> List[List[T]]:
        colors: defaultdict[T, str] = defaultdict(lambda: Colors.WHITE)

        def dfs_visit(n: T) -> List[T]:
            if colors[n] == Colors.WHITE:
                colors[n] = Colors.GRAY
                result = [n] + flatten(dfs_visit(neighbor) for neighbor in self.neighbors(n))
                colors[n] = Colors.BLACK
                return result
            else:
                return []

        result = []
        for n in sorted(self.nodes):
            if colors[n] == Colors.WHITE:
                result.append(dfs_visit(n))
        return result


    def kruskal(self) -> List[Edge[T]]:
        edges = [e for e in self.edgelist]
        heapq.heapify(edges)
        subcomponents = ComponentSets()
        mst = []
        for n in self.nodes:
            subcomponents.add(n)

        while len(mst) < (len(self.nodes) - 1) and edges:
            e = heapq.heappop(edges)
            assert e
            if subcomponents.representative(e.start) != subcomponents.representative(e.end):
                mst.append(e)
                subcomponents.union(e.start, e.end)

        return mst

    def prim(self, start=None) -> List[Edge[T]]:
        if start is None:
            start = self.nodes[0]
        result = []
        in_mst = set(start)
        next_edges = self.out_edges(start)
        heapq.heapify(next_edges)

        while len(result) < (len(self.nodes) - 1) and next_edges:
            e = heapq.heappop(next_edges)
            if e.end in in_mst:
                continue
            result.append(e)
            in_mst.add(e.end)
            for neighbor_edge in self.out_edges(e.end):
                if neighbor_edge.end not in in_mst:
                    heapq.heappush(next_edges, neighbor_edge)

        return result

    def check_mst(self, tree):
        edges = [e for e in self.edgelist]
        heapq.heapify(edges)
        min_edges = heapq.nsmallest(len(self.nodes) - 1, edges)
        min_mst_weight = sum(e.weight for e in min_edges)
        spanned_nodes = sorted(set(flatten((e.start, e.end) for e in tree)))
        is_full_span = len(self.nodes) == len(spanned_nodes)
        mst_weight = sum(e.weight for e in tree)

        return {
            'min_mst_weight': min_mst_weight,
            'spanned_nodes': spanned_nodes,
            'n_spanned_nodes': len(spanned_nodes),
            'is_full_span': is_full_span,
            'mst_weight': mst_weight,
        }

