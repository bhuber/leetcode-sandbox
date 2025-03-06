# https://neetcode.io/problems/sliding-window-maximum

# This solution too slow in python

from bisect import bisect_left
from typing import List


class Solution:
    def maxSlidingWindow(self, nums: List[int], k: int) -> List[int]:
        # 3 2 1 2 3, k = 3
        # [3 2 1] 2 3, m = 3
        # 3 [2 1 2] 3, m = 2
        # 3 2 [1 2 3], m = 3
        nums_len = len(nums)
        if nums_len == k:
            return [max(nums)]
        elif nums_len < k:
            return []

        current_counts = sorted(nums[:k])
        result = [current_counts[-1]]
        # loop invariant: current_counts = nums[sidx:eidx]
        sidx, eidx = 0, k
        while eidx < nums_len:
            #print(current_counts)
            drop_idx = bisect_left(current_counts, nums[sidx])
            assert current_counts[drop_idx] == nums[sidx]
            current_counts[drop_idx] = nums[eidx]
            current_counts.sort()
            result.append(current_counts[-1])
            sidx += 1
            eidx += 1
            #print(f"  {current_counts}, {sidx}, {eidx}")

        return result

