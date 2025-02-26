# https://leetcode.com/problems/number-of-islands/description/

from dataclasses import dataclass
from typing import Self, List

WHITE = "white"
GRAY = "gray"
BLACK = "black"

class Node:
    def __init__(self, row: int, col: int, is_land: bool):
        self.row = row
        self.col = col
        self.is_land = is_land
        self.neighbors: List[Node] = []

    def add_neighbor(self, node: Self):
        self.neighbors.append(node)

    def __repr__(self):
        neighbor_str = ",".join(n.coords() for n in self.neighbors)
        return f"({self.row}, {self.col}): " + ("1" if self.is_land else "0") + f" -> [{neighbor_str}]"

    def __str__(self):
        return self.__repr__()

    def coords(self):
        return f"({self.row}, {self.col})"

    _color = WHITE


class Graph:
    def __init__(self, land_matrix):
        self.node_matrix = []
        self.rows = len(land_matrix)
        self.cols = len(land_matrix[0]) if land_matrix else 0
        for r in range(0, self.rows):
            row = land_matrix[r]
            node_row = []
            self.node_matrix.append(node_row)
            n_cols = len(row)
            assert n_cols == self.cols

            for c in range(0, n_cols):
                node_row.append(Node(r, c, row[c] == "1"))

        for r in range(0, self.rows):
            for c in range(0, self.cols):
                node = self.node_matrix[r][c]
                if not node.is_land:
                    continue
                for maybe_neighbor in self._neighbors(r, c):
                    if maybe_neighbor.is_land:
                        node.add_neighbor(maybe_neighbor)

    def _neighbors(self, row: int, col: int):
        def in_bounds(row, col):
            return row >= 0 and row < self.rows and col >= 0 and col < self.cols

        pos_neighbors = [(row, col - 1), (row + 1, col), (row, col + 1), (row - 1, col)]
        return [self.node_matrix[row][col] for row, col in pos_neighbors if in_bounds(row, col)]

    def nodes(self):
        for r in range(0, self.rows):
            for c in range(0, self.cols):
                yield self.node_matrix[r][c]

    def n_islands(self):
        def dfs_recurse(n: Self):
            for neighbor in n.neighbors:
                if neighbor._color == WHITE:
                    neighbor._color = GRAY
                    dfs_recurse(neighbor)
                    neighbor._color = BLACK

        result = 0
        for n in self.nodes():
            if not n.is_land:
                continue
            if n._color == WHITE:
                result += 1
            dfs_recurse(n)

        return result




class Solution:
    def numIslands(self, grid: List[List[str]]) -> int:
        g = Graph(grid)
        print(g.node_matrix)
        return g.n_islands()
