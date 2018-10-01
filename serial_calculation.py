from __future__ import division
import math
import time
import copy

comp_cost = {0: 43090.589,
             1: 71702.323,
             2: 81004.102,
             3: 55960.300,
             4: 36018.857,
             5: 24993.789,
             6: 18201.324,
             7: 31468.431,
             8: 16990.050,
             9: 26677.609,
             10: 17115.513,
             11: 5713.572,
             12: 22254.892,
             13: 12507.182}

total = 0.00

for key, value in comp_cost.iteritems():
    total += value

print total