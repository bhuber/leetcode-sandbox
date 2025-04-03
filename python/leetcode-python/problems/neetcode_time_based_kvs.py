# https://neetcode.io/problems/time-based-key-value-store?uclick_id=1ac527c7-557a-40a7-aa0d-2111338cf29e

import bisect
from collections import defaultdict

class TimeMap:

    def __init__(self):
        self.tm: dict(str, list[(int, str)]) = {}


    def set(self, key: str, value: str, timestamp: int) -> None:
        vals = self.tm.get(key)
        if vals is None:
            vals = []
            self.tm[key] = vals
        return bisect.insort(vals, (timestamp, value))



    def get(self, key: str, timestamp: int) -> str:
        vals = self.tm.get(key)
        if vals is None:
            return ""

        idx = bisect.bisect_left(vals, timestamp, key=lambda t: t[0])
        #print(f"  {idx}")
        if idx < len(vals):
            if vals[idx][0] <= timestamp:
                # This should really only ever be ==, but either works
                return vals[idx][1]
            else:
                idx -= 1
                return vals[idx][1] if idx >= 0 else ''
        elif idx == len(vals) and vals[-1][0] <= timestamp:
            return vals[-1][1]
        else:
            return ''


tm = TimeMap()
def pg(k, ts):
    #print(f"k: {k}, ts: {ts}, r: {tm.get(k, ts)}")
    return
pg("alice", 1)           # return "happy"
pg("alice", 2)
tm.set("alice", "happy", 1)  # store the key "alice" and value "happy" along with timestamp = 1.
pg("alice", 1)           # return "happy"
pg("alice", 2)        # return "happy", there is no value stored for timestamp 2, thus we return the value at timestamp 1.
tm.set("alice", "sad", 3)   # store the key "alice" and value "sad" along with timestamp = 3.
pg("alice", 3)           # return "sad"
pg("alice", 1)          # return "happy"
pg("alice", 2)

#print(tm.tm)
#print('')