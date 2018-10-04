from __future__ import division
import math
import time
import copy

comp_cost = {0: 44523.971,
             1: 79379.446,
             2: 75741.272,
             3: 57830.227,
             4: 109292.856,
             5: 105682.034,
             6: 117613.441,
             7: 126152.932,
             8: 10901.276,
             9: 7470.036,
             10: 7112.192,
             11: 5794.625,
             12: 11782.275,
             13: 11604.194,
             14: 7001.366,
             15: 5869.689}

total = 0.00

for key, value in comp_cost.iteritems():
    total += value

print total