# https://neetcode.io/problems/binary-tree-maximum-path-sum

# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right

class State:
    def __init__(self, mps=None, mp=None, depth=None):
        self.max_path_sum = mps or 0
        self.max_path: List[TreeNode] = mp or []
        self.depth = depth or 0
        self.root_is_end = True

    def __iadd__(self, other):
        if other.depth - self.depth == 1:
            self.max_path_sum += other.max_path_sum
            self.max_path += other.max_path
        return self

    def __repr__(self):
        return ''.join(str(x) for x in
                       ['{max_path_sum: ', self.max_path_sum, ', max_path: ', [n.val for n in self.max_path], '}'])

    def __str__(self):
        return self.__repr__()


class Solution:
    def maxPathSum(self, root: Optional[TreeNode]) -> int:
        # post order traversal?
        # maxPathSum:
        #    maxpath(left) if > 0 + val + maxpath(right) if > 0
        result = self.max_path(root, State(float('-inf')))
        self.print_tree(root)
        print(result)
        return result.max_path_sum

    _mp_prefix = ''

    def max_path(self, root: Optional[TreeNode], state: State) -> State:
        if not root:
            return state

        self._mp_prefix += '  '
        state.depth += 1
        mpl = self.max_path(root.left, state)
        mpr = self.max_path(root.right, state)
        state.depth -= 1
        self._mp_prefix = self._mp_prefix[:-2]

        result = State(depth=state.depth)
        can_add_right = True
        if mpl.max_path_sum > mpr.max_path_sum and mpl.max_path_sum > 0:
            result += mpl
            can_add_right = False or (state.depth == 0)
        result += State(root.val, [root], depth=state.depth+1)
        if can_add_right and mpr.max_path_sum > 0:
            result += mpr


        print(f"{self._mp_prefix}{root.val}: {result}")
        return max([state, mpl, mpr, result], key=lambda s: s.max_path_sum)

    def print_tree(self, root: Optional[TreeNode], prefix=''):
        if not root:
            return

        print(prefix + str(root.val))
        prefix += '  '
        self.print_tree(root.left, prefix)
        self.print_tree(root.right, prefix)



"""
        if state.depth == 0:
            if mpl.max_path_sum > 0:
                result += mpl
            result += State(root.val, [root], depth=state.depth+1)
            if mpr.max_path_sum > 0:
                result += mpr
        else:
            can_add_right = True
            if mpl.max_path_sum > mpr.max_path_sum and mpl.max_path_sum > 0:
                result += mpl
                can_add_right = False
            result += State(root.val, [root], depth=state.depth+1)
            if can_add_right and mpr.max_path_sum > 0:
                result += mpr


        added_mpl = False
        if mpl.max_path_sum > 0:
            added_mpl = True
            result += mpl
        result += State(root.val, [root], depth=state.depth+1)
        if mpr.max_path_sum > 0:
            result += mpr
            result.root_is_end = not added_mpl
                """


