# - baseline 1: WTMB -> if schedulable, immediately schedule on any available processor
# (start serial, parallelizing in obvious way)
# Extreme preservation of locality at the cost of cpu utilization

from __future__ import division
import math

print "Start process of computing multi-processor schedule with baseline 1"

pnum = int(raw_input("Number of processors:"))
tnum = int(raw_input("Number of tasks:"))
arian = raw_input(("Input the single-thread schedule:"))

single_schedule = map(int, arian.split(' '))
print single_schedule
pr_schedule = []

graph = { 0: [2, 3],
          2: [],
          3: [4],
          4: [],
          1: [3]}


def find_edge(graph, start, end):
    # path = path + [start]
    if start == end:
        return False
    if not graph.has_key(start):
        return False
    if end in graph[start]:
        return True
    return False

# print find_edge(graph, 'A', 'C')
# print find_edge(graph, 'A', 'B')
# print find_edge(graph, 'E', 'D')


def baseline1(graph, pnum, tnum):

    l = int(math.ceil(tnum / pnum))

    # print l

    for n in range(pnum):
        pr_schedule.append([None] * l)
        # print(sum(x is None for x in pr_schedule[n]))
    # print pr_schedule

    for n in range(tnum):
        # raw_input("Press Enter to continue...")
        print "Now scheduling ", single_schedule[n]
        for m in range(n):
            if find_edge(graph, single_schedule[m], single_schedule[n]):
                print single_schedule[m], " to ", single_schedule[n], " found!"
                raw_input("Press Enter to continue...")
            else:
                pr_schedule
                continue


baseline1(graph, pnum, tnum)