# https://neetcode.io/problems/balanced-binary-tree
from typing import Optional


# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class Solution:
    def isBalanced(self, root: Optional[TreeNode]) -> bool:
        #self.print_tn(root)
        if not root:
            return True
        return self._is_balanced(root)[0]

    def _is_balanced(self, root: Optional[TreeNode]) -> (bool, int):
        def real_fn():
            nonlocal root
            if not root:
                return (True, 0)
            ibl = self._is_balanced(root.left)
            if not ibl[0]:
                # short circuit
                return (False, -1)
            ibr = self._is_balanced(root.right)
            return (ibl[0] and ibr[0] and (-1 <= (ibl[1] - ibr[1]) <= 1),
                    1 + max(ibl[1], ibr[1]))

        result = real_fn()
        #print(f"{root.val if root else None}: {result}")
        return result

    def print_tn(self, root: Optional[TreeNode], prefix=""):
        if not root:
            return
        print(prefix + str(root.val))
        if not (root.left or root.right):
            return
        else:
            self.print_tn(root.left, prefix + "  ")
            self.print_tn(root.right, prefix + "  ")


"""
                 1
        2                   2
    3                               3
  4   n                          n     4
"""