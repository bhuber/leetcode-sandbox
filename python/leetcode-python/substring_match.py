
class StringMatcherFA:
    # aaa = start -a> 1 -a> 2 -a> found
    #   [s 1 2 f]
    # s [* a - -]
    # 1 [* - a -]
    # 2 [* - - a]
    #
    # abac = start -a> 1 -b> 2 -a> 3 -b> 4
    #                    -a> 1 -a> 1
    #   [s 1 2 3 f]
    # s [* a - - -]  a
    # 1 [* a b - -]  ab
    # 2 [* - - a -]  aba
    # 3 [* a b - c]  abac
    #
    # * there are n+1 states
    # * start state is always default if nothing matches
    # * upper right triangle is always empty
    # * diagonal matches input string
    #
    # abacabad
    #   [s 1 2 3 4 5 6 7 f]
    # s [* a - - - - - - -]  a
    # 1 [* a b - - - - - -]  ab
    # 2 [* - - a - - - - -]  aba
    # 3 [* a b - c - - - -]  abac
    # 4 [* - - - - a - - -]  abaca
    # 5 [* a - - - - b - -]  abacab
    # 6 [* - - - - - - a -]  abacaba
    # 7 [* a b - c - - - d]  abacabad


    def __init__(self, s: str):
        self.states = set(c for c in s)


    def match(self, c: str) -> int:
        return -1

def substr_idx(full: str, to_find: str) -> int:
    return -1