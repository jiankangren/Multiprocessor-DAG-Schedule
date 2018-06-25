# h5: get an starting schedule from a* first, then re-compute with that fixed prefix every time
# a task is scheduled out of order.

from __future__ import division
import math
import time

tnum = 20

graph = {0: [7, 11],
          1: [11],
          2: [8, 9],
          3: [8, 9, 11, 7, 10, 12, 13],
          4: [10, 12, 13],
          5: [8, 9, 11, 7, 10 ,12, 13],
          6: [8, 9, 11],
          7: [14],
          8: [15],
          9: [14],
          10: [15, 17],
          11: [16],
          12: [],
          13: [16],
          14: [17, 18],
          15: [18, 19],
          16: [19],
          17: [],
          18: [],
          19: []}

g = {0: [3],
          1: [4, 2],
          2: [5, 3],
          3: [],
          4: [],
          5: []}

weight = {0: 1,
          1: 1,
          2: 1}


def find_path(graph,start,end, path=[]) :
    path=path+[start]
    if start==end :
        return path
    if not graph.has_key(start) :
        return None
    else :
        for node in graph[start] :
                 if node not in path:
                    newpath = find_path(graph, node, end, path)
                 if newpath :
                    return newpath
        return None


def find_all_ancestors(graph, target):
    ancestors = []
    task_list = list(range(0, tnum))
    for i in task_list:
            if i != target and find_path(graph, i, target):
                ancestors.append(i)
    
    return ancestors


def check_schedulable(graph, assigned_sofar, task):
    if set(assigned_sofar).issuperset(find_all_ancestors(graph, task)):
        return True
    else:
        return False


# Basically the get_cands function in paper.
def find_schedulables(graph, assigned_sofar):
    schedulables = []
    for task in range(tnum):
        if (task not in assigned_sofar) and check_schedulable(graph, assigned_sofar, task):
            schedulables.append(task)
    
    return schedulables

def find_edge(graph, start, end):
    # path = path + [start]
    if start == end:
        return False
    if not graph.has_key(start):
        return False
    if end in graph[start]:
        return True
    return False


def find_succesors(graph, target):
    successors = []
    task_list = list(range(0, tnum))
    for i in task_list:
            if i != target and find_edge(graph, target, i):
                successors.append(i)
    
    return successors

def max_distance(task, successors, assigned_sofar):
    u = assigned_sofar.index(task)
    temp = u
    #print "u is ", u
    for t in successors:
        if assigned_sofar.index(t) > temp:
            temp = assigned_sofar.index(t)
            #print temp," for task ", t
    return temp - u

def find_successors(graph, target):
    successors = []
    task_list = list(range(0, tnum))
    for i in task_list:
            if i != target and find_edge(graph, target, i):
                successors.append(i)
    
    return successors

def tmb_cost(graph, assigned_sofar):
    #schedulables = find_schedulables(graph, assigned_sofar)
    tmb = 0
    for task in assigned_sofar:
        successors = find_successors(graph, task)
        if successors == []:
            print "Triggerred 1, no successors"
            continue
        elif set(assigned_sofar).issuperset(successors):
            tmb += max_distance(task, successors, assigned_sofar)
            print "Triggerred 2, all successors scheduled"
        else:
            tmb += len(assigned_sofar) - assigned_sofar.index(task)
            print "Triggerred 3"

        print "Task ", task, " cost has been added, tmb is now ", tmb
    return tmb


if __name__ == "__main__":
    # print find_path(graph, 0, 18)
    # print find_all_ancestors(graph, 8)
    # print find_all_ancestors(graph, 15)
    # print check_schedulable(graph, [3,2,0,5], 8)
    # print find_schedulables(graph, [3,2,5])
    # print find_schedulables(graph, [3,2,5,6])
    # print find_succesors(graph, 4)
    # print max_distance(4, [10,12,13], [0,4,10,6,13,8,7,12])
    print tmb_cost(g, [0,1,2,4])
  #find_all_ancestors(graph, 10)