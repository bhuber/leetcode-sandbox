# https://neetcode.io/problems/rotting-fruit

from collections import deque
from typing import Tuple, List

EMPTY = 0
FRESH = 1
ROTTEN = 2


class Solution:
    def orangesRotting(self, grid: List[List[int]]) -> int:
        # bfs, with start points as rotting nodes
        # return max depth reached before all cells visited
        rows = len(grid)
        cols = len(grid[0])

        def valid_coords(r, c):
            return r >= 0 and r < rows and c >= 0 and c < cols

        def neighbors(r, c):
            maybe_coords = [(r, c + 1), (r + 1, c), (r, c - 1), (r - 1, c)]
            return [(row, col) for row, col in maybe_coords if valid_coords(row, col) and grid[row][col] == FRESH]

        next_nodes = deque()
        total_fruit = 0
        starting_fresh = 0
        for r in range(0, rows):
            row = grid[r]
            for c in range(0, cols):
                if row[c] == ROTTEN:
                    next_nodes.append({'depth': 0, 'coords': (r, c)})
                    row[c] = FRESH # set it fresh to start, makes loop logic below easier
                    total_fruit += 1
                elif row[c] == FRESH:
                    total_fruit += 1
                    starting_fresh += 1

        #print(f"tf: {total_fruit}, sf: {starting_fresh}")
        fruits_rotted = 0
        max_depth = 0
        while fruits_rotted < total_fruit and len(next_nodes) > 0:
            current_node = next_nodes.popleft()
            current_node_coords = current_node['coords']
            if grid[current_node_coords[0]][current_node_coords[1]] != FRESH:
                continue

            #print(current_node)
            grid[current_node_coords[0]][current_node_coords[1]] = ROTTEN
            fruits_rotted += 1
            max_depth = current_node['depth']
            next_nodes.extend({'depth': current_node['depth'] + 1, 'coords': coords}
                              for coords in neighbors(*current_node_coords))
            #print(next_nodes)

        return max_depth if fruits_rotted == total_fruit else -1