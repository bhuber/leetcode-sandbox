from typing import Tuple, List, Callable, Set
import inspect


def _board_str(board: List[List[int]]) -> str:
    return "[" + "\n ".join(str(r) for r in board) + "]"

class FirstSolution:
    # This is the original interview solution, as best I can recall, with some extra modifications
    # It fails test2 below

    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.rests = [[0] * cols for _ in range(rows)]
        self.islands = [[0] * cols for _ in range(rows)]
        self.n_islands = 0
        self.next_island_id = 1
        self.island_roots = {}

    def open_restaurant(self, r: int, c: int):
        self.rests[r][c] += 1
        if self.rests[r][c] > 1:
            # Already counted in islands, do nothing
            return

        neighbor_islands = set()
        for nr, nc in self._neighbors(r, c):
            ni = self.islands[nr][nc]
            if ni != 0:
                neighbor_islands.add(ni)

        if not neighbor_islands:
            self.n_islands += 1
            self.islands[r][c] = self.next_island_id
            self.island_roots[self.next_island_id] = self.next_island_id
            self.next_island_id += 1
        else:
            self._update_neighbor_islands(r, c, neighbor_islands)

    def _update_neighbor_islands(self, r: int, c: int, neighbor_islands: Set[int]):
        # This was inlined in original solution, and contains the bug
        root = min(neighbor_islands)
        self.islands[r][c] = root
        for ni in neighbor_islands:
            if self.island_roots[ni] != root:
                self.island_roots[ni] = root
                self.n_islands -= 1

    def delivery_zones(self):
        return self.n_islands

    def _neighbors(self, r: int, c: int) -> List[Tuple[int, int]]:
        return [(r_, c_) for (r_, c_) in [(r + 1, c), (r, c - 1), (r - 1, c), (r, c + 1)]
                if 0 <= r_ < self.rows and 0 <= c_ < self.cols]


    def __repr__(self):
        return f"class: {type(self).__name__}, n_islands: {self.n_islands}\nrests:\n{_board_str(self.rests)}\nislands:\n{_board_str(self.islands)}\nroots:\n{self.island_roots}"

    def __str__(self):
        return self.__repr__()



class CorrectSolution(FirstSolution):
    # Better solution, which is the same as the original, but with fixed logic for
    # _update_neighbor_islands. It still contains a bug though

    def _update_neighbor_islands(self, r: int, c: int, neighbor_islands: Set[int]):
        # PRE and POST conditions:
        #  1. Each island id appears in exactly 1 logical island
        #  2. for each island_id within a given logical island i,
        #    self.island_roots[island_id] == min(island_id for island_id in island),
        #    i.e. the root of every island id in a given island is the min id for that island
        #  3. PRE 2) => Each chain in self.island_roots is of length 0 or 1.
        #    i.e. either self.island_roots[x] == x, or self.island_roots[self.island_roots[x]] == self.island_roots[x]

        # each entry in neighbor_islands is an island_id in an island that is being merged together
        # in this function.  PRE 2) implies that the min of their roots will be the min island_id for
        # their new merged island
        root = min(self.island_roots[i] for i in neighbor_islands)
        self.islands[r][c] = root
        for ni in neighbor_islands:
            if self.island_roots[ni] != root:
                # All islands get merged into the island with smallest id (i.e. root)
                # This is the merge logic.

                # Update the roots as necessary.
                # For example, if we have island_roots \superset {4: 3, 3: 3}, root = 1, and ni = 4,
                # we need to update both island_roots[4] and island_roots[3].
                # By PRE 3), we don't have to search any deeper.
                # Note the order matters here, we have to update the parent before the child
                self.island_roots[self.island_roots[ni]] = root
                self.island_roots[ni] = root

                # When an island is merged into another, we have one less island
                self.n_islands -= 1


class SimpleAssert:
    # I don't think this repl can run unit tests, so this is just the dumbest assert lib imaginable
    def __init__(self):
        self.passed = True

    def eq(self, expected, actual, message=None, eq=lambda x, y: x == y):
        if not eq(expected, actual):
            self.passed = False
            print(f"ERROR line {inspect.stack()[1].lineno}: {expected} != {actual}")
            if message:
                print("  " + message)


def test1(make_s: Callable[[int, int], FirstSolution]):
    # Test used in interview, both solutions pass

    # 4x4 grid, with restaurants added in order below:
    # 0 0 0 0
    # 0 1 0 0
    # 0 4 3 2
    # 0 0 0 0
    print("test1...")
    a = SimpleAssert()
    s = make_s(4, 4)

    a.eq(s.delivery_zones(), 0)
    s.open_restaurant(1, 1)
    a.eq(s.delivery_zones(), 1)
    s.open_restaurant(2, 3)
    a.eq(s.delivery_zones(), 2)
    s.open_restaurant(2, 2)
    a.eq(s.delivery_zones(), 2)
    s.open_restaurant(2, 1)
    a.eq(s.delivery_zones(), 1)

    if not a.passed:
        print(s)
    print("DONE test1")


def test2(make_s: Callable[[int, int], FirstSolution]):
    # New test demonstrating bug, FirstSolution fails

    # 5x5 grid, with restaurants added in order below:
    # 0 0 0 0 0
    # 0 1 0 0 0
    # 2 5 4 0 0
    # 0 3 6 0 0
    # 0 0 0 0 0
    print("test2...")
    a = SimpleAssert()
    s = make_s(5, 5)

    a.eq(s.delivery_zones(), 0)
    s.open_restaurant(1, 1)
    a.eq(s.delivery_zones(), 1)
    s.open_restaurant(2, 0)
    a.eq(s.delivery_zones(), 2)
    s.open_restaurant(3, 1)
    a.eq(s.delivery_zones(), 3)
    s.open_restaurant(2, 2)
    a.eq(s.delivery_zones(), 4)
    s.open_restaurant(2, 1)
    a.eq(s.delivery_zones(), 1)
    s.open_restaurant(3, 2)
    a.eq(s.delivery_zones(), 1)

    if not a.passed:
        print(s)
    print("DONE test2")


def test3(make_s: Callable[[int, int], FirstSolution]):
    # New test demonstrating *another* bug, FirstSolution and CorrectSolution fail

    # 5x5 grid, with restaurants added in order below:
    # 0 0 0 0 0
    # 1 0 4 0 0
    # 3 0 6 8 0
    # 2 7 5 9 0
    # 0 0 0 0 0
    print("test3...")
    a = SimpleAssert()
    s = make_s(5, 5)
    a.eq(s.delivery_zones(), 0)

    s.open_restaurant(1, 0)
    a.eq(s.delivery_zones(), 1)
    s.open_restaurant(3, 0)
    a.eq(s.delivery_zones(), 2)
    s.open_restaurant(2, 0)
    a.eq(s.delivery_zones(), 1)

    s.open_restaurant(1, 2)
    a.eq(s.delivery_zones(), 2)
    s.open_restaurant(3, 2)
    a.eq(s.delivery_zones(), 3)
    s.open_restaurant(2, 2)
    a.eq(s.delivery_zones(), 2)

    s.open_restaurant(3, 1)
    a.eq(s.delivery_zones(), 1)

    s.open_restaurant(2, 3)
    a.eq(s.delivery_zones(), 1)
    s.open_restaurant(3, 3)
    a.eq(s.delivery_zones(), 1)

    #if not a.passed:
    print(s)
    print("DONE test3")


print("Test FirstSolution")
test1(FirstSolution)
test2(FirstSolution)
test3(FirstSolution)

print()
print("Test CorrectSolution")
test1(CorrectSolution)
test2(CorrectSolution)
test3(CorrectSolution)
