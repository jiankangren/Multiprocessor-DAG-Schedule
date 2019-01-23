from __future__ import division
import math
import time
import copy

d6 = {0: [12], 1: [12], 2: [12], 3: [12], 4: [19], 5: [19], 6: [19], 7: [19],
         8: [19], 9: [19], 10: [19], 11: [19], 12: [13, 14, 15, 16, 17, 18],
         13: [14], 14: [18], 15: [18], 16: [18], 17: [18], 18: [], 19: [18]}

d3 = { 0: [4, 8], 1: [8], 2: [13, 17], 3: [17], 4: [5, 6, 7], 5: [], 6: [],
          7: [], 8: [9, 17], 9: [10, 11, 12], 10: [], 11: [], 12: [], 13: [14, 15, 16],
          14: [], 15: [], 16: [], 17: [18], 18: [19, 20, 21], 19: [], 20: [], 21: []}

d1 = {0: [7, 11], 1: [11], 2: [8, 9], 3: [8, 9, 11, 7, 10, 12, 13], 4: [10, 12, 13],
         5: [8, 9, 11, 7, 10, 12, 13], 6: [8, 9, 11], 7: [], 8: [], 9: [], 10: [], 11: [], 12: [], 13: []}

d5 = {0: [1],
         1: [2],
         2: [3],
         3: [4],
         4: [5, 6, 8, 10, 12],
         5: [],
         6: [7],
         7: [],
         8: [9],
         9: [],
         10: [11],
         11: [],
         12: [13],
         13: []}

graph = {0: [9, 13, 20],
          1: [13],
          2: [10, 11],
          3: [9, 10, 11, 12, 13, 14, 15, 19],
          4: [12, 14, 15, 18],
          5: [9, 10, 11, 12, 13, 14, 15],
          6: [10, 11, 13],
          9: [16],
          10: [16],
          11: [16],
          12: [16],
          13: [16],
          14: [16],
          15: [16],
          16: [17],
          17: [18, 19, 20],
          18: [21],
          19: [21],
          20: [21],
          21: [22],
          22: [],
          7: [23, 24, 25, 26],
          8: [27, 28, 29, 30],
          23: [31, 32],
          24: [31, 33],
          25: [31, 34],
          26: [31, 35],
          27: [31, 36],
          28: [31, 37],
          29: [31, 38],
          30: [31, 39],
          31: [],
          32: [40],
          33: [40],
          34: [40],
          35: [40],
          36: [40],
          37: [40],
          38: [40],
          39: [40],
          40: []}

comp_cost = {0: 2.92,
          1: 0.225,
          2: 5.623,
          3: 0.011,
          4: 4.039,
          5: 0.054,
          6: 0.001,
          7: 1.511,
          8: 0.102,
          9: 0.001,
          10: 0.001,
          11: 0.001,
          12: 0.001,
          13: 0.001,
          14: 0.001,
          15: 0.001,
          16: 0.001,
          17: 0.001,
          18: 0.001,
          19: 0.001,
          20: 0.001,
          21: 0.001,
          22: 0.001,
          23: 0.001,
          24: 0.001,
          25: 0.001,
          26: 0.001,
          27: 0.001,
          28: 0.001,
          29: 0.001,
          30: 0.001,
          31: 0.001,
          32: 0.001,
          33: 0.001,
          34: 0.001,
          35: 0.001,
          36: 0.001,
          37: 0.001,
          38: 0.001,
          39: 0.001,
          40: 0.001}

schedule = [[6, 10,13,12,18,22,24,8,27,39,40],
            [5, 11,9,14,20,7,25,30,29,38],
            [3, 0,4,16,19,23,34,28,31,35],
            [2, 1,15,17,21,26,33,32,36,37]]

time_table = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0,
              10: 0, 11: 0, 12: 0, 13: 0, 14: 0, 15: 0, 16: 0, 17: 0, 18: 0, 19: 0, 20: 0, 21: 0,
              22: 0, 23: 0, 24: 0, 25: 0, 26: 0, 27: 0, 28: 0, 29: 0, 30: 0, 31: 0,
              32: 0, 33: 0, 34: 0, 35: 0, 36: 0, 37: 0, 38: 0, 39: 0, 40: 0}


def callback(key, value):
    pass
    #print (key, value)

pnum = 4
tnum = 14
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
        previous_in_schedule = time_of_task(graph, processor[idx-1])
        if previous_in_schedule > parent_time:
            parent_time = previous_in_schedule
        end_time = parent_time + cost_of_task(graph, processor[idx])
        #print "End time for task ", processor[idx], " is ", end_time
        time_table[processor[idx]] = end_time

    return end_time

for i in range(tnum):
    print time_of_task(graph, i)

print time_table