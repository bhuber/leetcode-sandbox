# https://neetcode.io/problems/valid-tree
from typing import List

WHITE = "white"
GRAY = "gray"
BLACK = "black"

class NotATreeException(Exception):
    pass

class Solution:
    def validTree(self, n: int, edges: List[List[int]]) -> bool:
        # tree there is exactly one path from every node to every other node
        # dfs - color nodes - if we hit a gray or black node during recursion, we know there's some other path to it
        # need to discount immediate predecessor

        node_neighbors = [list() for _ in range(n)]
        for e in edges:
            node_neighbors[e[0]].append(e[1])
            node_neighbors[e[1]].append(e[0])

        #print(node_neighbors)

        node_colors = [WHITE] * n
        nodes_visited = 0
        prefix = ''

        def dfs(node: int, predecessor: int):
            nonlocal prefix
            nonlocal nodes_visited
            node_colors[node] = GRAY
            #print(prefix + str(node))
            prefix += '  '
            for neighbor in node_neighbors[node]:
                if neighbor == predecessor:
                    continue
                if node_colors[neighbor] != WHITE:
                    #print(f"NOT A TREE: neigh {neighbor}, colors {node_colors}")
                    raise NotATreeException()
                dfs(neighbor, node)

            node_colors[node] = BLACK
            nodes_visited += 1
            prefix = prefix[0:-2]

        try:
            dfs(0, -1)
            return nodes_visited == n
        except NotATreeException as e:
            return False