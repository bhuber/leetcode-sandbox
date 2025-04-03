# https://leetcode.com/problems/coin-change/?envType=study-plan-v2&envId=top-interview-150

import functools
from typing import List


class Solution:
    coins: List[int]

    def coinChange(self, coins: List[int], amount: int) -> int:
        self.coins = sorted(coins, reverse=True)
        print(f"coins: {self.coins}")
        result = self._coinChange(amount)
        return len(result) if result is not None else -1

    @functools.cache
    def _coinChange(self, amount: int) -> List[int]:
        #print(f"amount: {amount}")
        # greedy algorithm
        # always pick biggest denomination possible, then return that + coinChange(remainder)
        if amount == 0:
            return []
        else:
            results = []
            for c in self.coins:
                if amount >= c:
                    result = self._coinChange(amount - c)
                    if result is not None:
                        results.append([c] + result)
                        if self.coins[0] == 1:
                            break
            if results:
                return min(results, key=len)

            return None
