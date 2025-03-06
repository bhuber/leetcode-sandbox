# https://neetcode.io/problems/permutation-string

from collections import defaultdict
from copy import copy
from typing import Dict


class Solution:
    def checkInclusion(self, s1: str, s2: str) -> bool:
        # sort s1
        # slide right:
        #   remove leftmost character from current string
        #   add rightmost char to current string
        #   keep count of diff of current from s1
        # lecaabee
        # |cel|aabee
        # l|ace|abee
        # le|aac|bee
        s1_len = len(s1)
        if s1_len > len(s2):
            return False
        elif s1_len == 0:
            return True

        s1_char_counts: Dict[str, int] = defaultdict(lambda: 0)
        curr_char_counts: Dict[str, int] = defaultdict(lambda: 0)
        match_count = 0
        for c in s1:
            s1_char_counts[c] += 1

        def add_char(c: str) -> bool:
            nonlocal s1_char_counts, curr_char_counts, match_count
            s1_count = s1_char_counts.get(c)
            if s1_count:
                curr_char_counts[c] += 1
                curr_count = curr_char_counts[c]
                print(f"add_char: {c}, {curr_count}")
                if curr_count <= s1_count:
                    match_count += 1
                    print(f"  add_char: {match_count}")
                    if match_count == s1_len:
                        return True

            return False

        def remove_char(c: str):
            nonlocal s1_char_counts, curr_char_counts, match_count
            s1_count = s1_char_counts.get(c)
            if s1_count:
                curr_char_counts[c] -= 1
                curr_count = curr_char_counts[c]
                assert curr_char_counts[c] >= 0
                if curr_count < s1_count:
                    match_count -= 1
                    assert match_count >= 0


        for c in s2[:s1_len]:
            if add_char(c):
                return True

        print(s1_char_counts)
        print(curr_char_counts)

        # sidx is first char of current string, eidx is last char of current string
        sidx, eidx = 0, s1_len - 1
        print(f"({sidx}, {eidx}), \"{s2[sidx:eidx+1]}\", {match_count}, {dict(curr_char_counts)}")
        while eidx < len(s2) - 1:
            remove_char(s2[sidx])
            sidx += 1
            eidx += 1
            if add_char(s2[eidx]):
                print(f"({sidx}, {eidx}), \"{s2[sidx:eidx+1]}\"")
                return True
            print(f"({sidx}, {eidx}), \"{s2[sidx:eidx+1]}\", {match_count}, {dict(curr_char_counts)}")

        return False