from __future__ import division
import math
import time
import copy

graph = {0: [12], 1: [12], 2: [12], 3: [12], 4: [19], 5: [19], 6: [19], 7: [19],
         8: [19], 9: [19], 10: [19], 11: [19], 12: [13, 14, 15, 16, 17, 18],
         13: [14], 14: [18], 15: [18], 16: [18], 17: [18], 18: [], 19: [18]}

d3 = { 0: [4, 8], 1: [8], 2: [13, 17], 3: [17], 4: [5, 6, 7], 5: [], 6: [],
          7: [], 8: [9, 17], 9: [10, 11, 12], 10: [], 11: [], 12: [], 13: [14, 15, 16],
          14: [], 15: [], 16: [], 17: [18], 18: [19, 20, 21], 19: [], 20: [], 21: []}

d5 = {0: [7, 11], 1: [11], 2: [8, 9], 3: [8, 9, 11, 7, 10, 12, 13], 4: [10, 12, 13],
         5: [8, 9, 11, 7, 10, 12, 13], 6: [8, 9, 11], 7: [], 8: [], 9: [], 10: [], 11: [], 12: [], 13: []}

d6 = {0: [1],
         1: [2],
         2: [3, 7],
         3: [],
         4: [5],
         5: [6, 7],
         6: [],
         7: [8, 12],
         8: [9],
         9: [10],
         10: [11],
         11: [],
         12: [13],
         13: [14],
         14: [15],
         15: []}

comp_cost = {0: 84418.179,
          1: 5974.676,
          2: 143017.434,
          3: 341.889,
          4: 197405.492,
          5: 67036.553,
          6: 14141.704,
          7: 4720.618,
          8: 410.982,
          9: 9127.021,
          10: 988.125,
          11: 541.956,
          12: 34845.233,
          13: 38836.522,
          14: 44548.561,
          15: 39385.079,
          16: 43703.135,
          17: 90075.421,
          18: 7344.402,
          19: 137290.097}

schedule = [[3,0,6,9,16], [8,1,5,7,17], [11,2,12,13,19], [10,4,15,14,18]]

time_table = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0,
              10: 0, 11: 0, 12: 0, 13: 0, 14: 0, 15: 0, 16: 0, 17: 0, 18: 0, 19: 0}

def callback(key, value):
    pass
    #print (key, value)

pnum = 4
tnum = 20
finished_so_far = []


def find_edge(graph, start, end):
    # path = path + [start]
    if start == end:
        return False
    if not graph.has_key(start):
        return False
    if end in graph[start]:
        return True
    return False


def find_all_ancestors(graph, target):
    ancestors = []
    task_list = list(range(0, tnum))
    for i in task_list:
        if i != target and (find_edge(graph, i, target) != False):
            ancestors.append(i)
    return ancestors



def cost_of_task(graph, task):
    cost = comp_cost[task]

    return cost


def time_of_task(graph, task):

    # Find task in schedule first.
    for each_core in schedule:
        for i in range(0, len(each_core)):
            if each_core[i] == task:
                processor = copy.copy(each_core)
                idx = copy.copy(i)
                #print " -- Found task ", task, " at ", idx, " on ", processor
                break
        else:
            continue
        break

    end_time = 0.0
    parent_time = 0.0
    temp = 0.0
    #print "THIS IS ", processor[idx]
    ancestors = find_all_ancestors(graph, processor[idx])
    if not ancestors:
        # A base table query, the end time should be end_time of
        # previous task in processor + cost of this task
        if idx != 0:
            end_time = time_of_task(graph, processor[idx-1]) + cost_of_task(graph, processor[idx])
            #print "Case: base query NOT at start of process. End time for task ", processor[idx], " is ", end_time
            time_table[processor[idx]] = end_time
        else:
            end_time = cost_of_task(graph, processor[idx])
            #print "Case: base query at start of process. End time for task ", processor[idx], " is ", end_time
            time_table[processor[idx]] = end_time

    else:
        for parent in ancestors:
            temp = time_of_task(graph, parent)
            if temp > parent_time:
                parent_time = temp
                #print "Case: non-base query. Parent task: ", parent, " time is: ", parent_time

        end_time = parent_time + cost_of_task(graph, processor[idx])
        #print "End time for task ", processor[idx], " is ", end_time
        time_table[processor[idx]] = end_time

    return end_time

for i in range(tnum):
    print time_of_task(graph, i)

print time_table