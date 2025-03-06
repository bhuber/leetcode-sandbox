# https://neetcode.io/problems/foreign-dictionary

from typing import List
from collections import defaultdict

class Solution:
    def foreignDictionary(self, words: List[str]) -> str:
        # graph with each character as node
        # topo sort graph
        # how to determine edges
        # for each pair of words, find first character that differs.  That's an edge.
        # Invalid inputs will create graphs with cycles

        # toposort:
        # dfs all nodes
        # remove start nodes for contention as they have incoming edges

        if len(words) == 0:
            return ""
        elif len(words) == 1:
            return words[0] if len(words[0]) == 1 else ""

        #adj_list = {chr(i): set() for i in range(ord('a'), ord('z') + 1)}
        adj_list = defaultdict(set)
        for i in range(len(words) - 1):
            current_word = words[i]
            next_word = words[i + 1]
            for j in range(min(len(current_word), len(next_word))):
                if current_word[j] != next_word[j]:
                    adj_list[current_word[j]].add(next_word[j])
                    break
                else:
                    _ = adj_list[current_word[j]]

            if len(current_word) > len(next_word) and j + 1 == len(next_word):
                #print(f"cw: {current_word}, nw: {next_word}")
                return ""

            for k in range(j + 1, len(current_word)):
                _ = adj_list[current_word[k]]

        last_word = words[-1]
        for c in last_word:
            _ = adj_list[c]

        color = {c: 'white' for c in adj_list.keys()}
        done_nodes = []
        #print(f"adj_list: {adj_list}, color: {color}")

        def dfs(node: str) -> bool:
            color[node] = 'gray'
            for neighbor in adj_list[node]:
                if color[neighbor] == 'white':
                    if not dfs(neighbor):
                        return False
                elif color[neighbor] == 'gray':
                    # cycle detected
                    return False

            color[node] = 'black'
            done_nodes.append(node)
            return True

        cycle_detected = False
        for n in adj_list.keys():
            if color[n] == 'white':
                cycle_detected = cycle_detected or not dfs(n)

        if cycle_detected:
            return ''
        else:
            done_nodes.reverse()
            return ''.join(done_nodes)

