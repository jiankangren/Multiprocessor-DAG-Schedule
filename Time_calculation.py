from __future__ import division
import math
import time
import copy

d4 = {0: [12], 1: [12], 2: [12], 3: [12], 4: [19], 5: [19], 6: [19], 7: [19],
         8: [19], 9: [19], 10: [19], 11: [19], 12: [13, 14, 15, 16, 17, 18],
         13: [14], 14: [18], 15: [18], 16: [18], 17: [18], 18: [], 19: [18]}

graph = { 0: [4, 8], 1: [8], 2: [13, 17], 3: [17], 4: [5, 6, 7], 5: [], 6: [],
          7: [], 8: [9, 17], 9: [10, 11, 12], 10: [], 11: [], 12: [], 13: [14, 15, 16],
          14: [], 15: [], 16: [], 17: [18], 18: [19, 20, 21], 19: [], 20: [], 21: []}

d1 = {0: [7, 11], 1: [11], 2: [8, 9], 3: [8, 9, 11, 7, 10, 12, 13], 4: [10, 12, 13],
         5: [8, 9, 11, 7, 10, 12, 13], 6: [8, 9, 11], 7: [], 8: [], 9: [], 10: [], 11: [], 12: [], 13: []}

comp_cost = {0: 28350.958,
             1: 8052.327,
             2: 77246.003,
             3: 2029.837,
             4: 17757.023,
             5: 9385.720,
             6: 9748.652,
             7: 11488.475,
             8: 36521.805,
             9: 99791.186,
             10: 27053.805,
             11: 29586.301,
             12: 47146.810,
             13: 102256.968,
             14: 17654.645,
             15: 52273.527,
             16: 31150.638,
             17: 34053.565,
             18: 65795.944,
             19: 31642.782,
             20: 27397.375,
             21: 29767.535}

schedule = [[0,1,2,17,16,20],[4,3,9,10,14,21],[6,8,13,11,18],[7,5,12,15,19]]

time_table = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0,
              10: 0, 11: 0, 12: 0, 13: 0, 14: 0, 15: 0, 16: 0, 17: 0, 18: 0, 19: 0, 20: 0, 21: 0}


def callback(key, value):
    pass
    #print (key, value)

pnum = 4
tnum = 22
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