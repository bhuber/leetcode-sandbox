# https://leetcode.com/problems/word-search/?uclick_id=1ac527c7-557a-40a7-aa0d-2111338cf29e

from typing import List, Tuple


class Solution:
    def exist(self, board: List[List[str]], word: str) -> bool:
        # bfs, roots are starting letter of word
        # mark coords using 2d bool array
        if not board or not board[0]:
            return False
        if len(word) == 0:
            return True

        self.board = board
        self.word = word
        self.word_len = len(word)
        self.height = len(board)
        self.width = len(board[0])
        self.marked = set()

        for r in range(self.height):
            for c in range(self.width):
                if self.dfs((r, c), 0):
                    return True

        return False

    def neighbors(self, r: int, c: int) -> List[Tuple[int, int]]:
        return [(r_, c_) for (r_, c_) in [(r, c + 1), (r - 1, c), (r, c - 1), (r + 1, c)]
                if 0 <= r_ < self.height and 0 <= c_ < self.width]

    def idx(self, coords: Tuple[int, int]) -> str:
        return self.board[coords[0]][coords[1]]

    def dfs(self, root: Tuple[int, int], word_idx: int) -> bool:
        #print(f"dfs_enter({root}, {word_idx})")
        if self.board[root[0]][root[1]] != self.word[word_idx] or root in self.marked:
            #print(f"dfs({root}, {word_idx})(idx: {self.idx(root)}, ch: {self.word[word_idx]}) = False")
            return False
        if (word_idx == self.word_len - 1):
            #print(f"dfs({root}, {word_idx}) = True")
            return True

        self.marked.add(root)
        #print(f"  n: {self.neighbors(*root)}")
        for n in self.neighbors(*root):
            if self.dfs(n, word_idx + 1):
                return True
        self.marked.remove(root)
        return False

from collections import Counter

class SolutionFast:
    # Beats like 98% of solutions, ~2000x faster than above solution
    def exist(self, board: List[List[str]], word: str) -> bool:
        m, n, k = len(board[0]), len(board), len(word)
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        word_histogram = Counter()
        for ch in word:
            word_histogram[ch] += 1

        # Reverse word if last character is less frequent than first
        # to reduce recursion calls
        if word_histogram[word[0]] > word_histogram[word[-1]]:
            word = word[::-1]

        grid_histogram = Counter()
        start_idxs = []
        for i in range(n):
            for j in range(m):
                ch = board[i][j]
                grid_histogram[ch] += 1
                if word[0] == ch:
                    # Since we're already walking the grid once, remember
                    # where potential words start. This does waste memory
                    # in the worst case, but rarely, and only O(n)
                    start_idxs.append((i, j))

        # If there aren't enough occurrences of any letter in the search word
        # in the grid, we know we'll never find it
        for key, val in word_histogram.items():
            if grid_histogram[key] < val:
                return False

        def dfs(i, j, pos):
            # Note pos is offset by 1, as we assume we've already checked word[0]
            # before first call
            if pos == k - 1:
                return True
            temp = board[i][j]
            board[i][j] = ""
            for d in directions:
                i_, j_ = i + d[0], j + d[1]
                if 0 <= i_ < n and 0 <= j_ < m and board[i_][j_] == word[pos+1]:
                    if dfs(i_, j_, pos + 1): return True
            board[i][j] = temp
            return False

        for i, j in start_idxs:
            if dfs(i, j, 0):
                return True

        return False