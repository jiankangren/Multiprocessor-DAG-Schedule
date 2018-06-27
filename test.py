# h3: get an starting schedule from a* first, then re-compute with that fixed prefix every time
# a task is scheduled out of order.

from __future__ import division
import math
import time
import copy


print "Start process of computing multi-processor schedule with heuristic 3"

pnum = int(raw_input("Number of processors:"))
tnum = int(raw_input("Number of tasks:"))
arian = raw_input(("Enter the starting single-thread schedule:"))
single_schedule = map(int, arian.split(' '))

print single_schedule

single_schedule_intact = list(single_schedule)

assigned_sofar = list()
finished_sofar = list()

delayed_index = list()
delayed = list()

pr_schedule = []

# DAG1 - 7Q
d1 = {0: [7, 11],
         1: [11],
         2: [8, 9],
         3: [8, 9, 11, 7, 10, 12, 13],
         4: [10, 12, 13],
         5: [8, 9, 11, 7, 10, 12, 13],
         6: [8, 9, 11],
         7: [],
         8: [],
         9: [],
         10: [],
         11: [],
         12: [],
         13: []}


# DAG2 - Deeper 7Q
d2 = {0: [7, 11],
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

# DAG3 from Arian
d3 = { 0: [4, 8],
          1: [8],
          2: [13, 17],
          3: [17],
          4: [5, 6, 7],
          5: [],
          6: [],
          7: [],
          8: [9, 17],
          9: [10, 11, 12],
          10: [],
          11: [],
          12: [],
          13: [14, 15, 16],
          14: [],
          15: [],
          16: [],
          17: [18],
          18: [19, 20, 21],
          19: [],
          20: [],
          21: []}

#SIPHT i.e. dag4.
d4  = {0: [12],
         1: [12],
         2: [12],
         3: [12],
         4: [19],
         5: [19],
         6: [19],
         7: [19],
         8: [19],
         9: [19],
         10: [19],
         11: [19],
         12: [13, 14, 15, 16, 17, 18],
         13: [14],
         14: [18],
         15: [18],
         16: [18],
         17: [18],
         18: [],
         19: [18]}

# Example graph.
graph = {0: [3],
     1: [4, 2],
     2: [5, 3],
     3: [],
     4: [],
     5: []}

weight = {0: 1,
          1: 1,
          2: 1}

# def wtmb_edge(graph, weight, start, end):
#     if end in graph[start]:
#         return weight[start]*1
#     else if find_edge():

def pr_schedule_init(pnum, tnum):
    l = int(math.ceil(tnum / pnum))
    # print l

    for n in range(pnum):
        pr_schedule.append([None] * l)
    print(sum(x is None for x in pr_schedule[n]))
    print pr_schedule


# Need to be able to find edges with >1 length.
#def find_edge(graph, start, end):
    # path = path + [start]
#    if start == end:
#        return False
#    if not graph.has_key(start):
#        return False
#    if end in graph[start]:
#        return True
#    return False

# Only finds successors.
def find_edge(graph, start, end):
    # path = path + [start]
    if start == end:
        return False
    if not graph.has_key(start):
        return False
    if end in graph[start]:
        return True
    return False

# Finds grandchildren as well.
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

# Basically the same as check_schedulable.
def find_dependencies(graph, assigned_sofar, task):
    flag = False
    for assigned in assigned_sofar:
        if find_path(graph, assigned, task):
            flag = True
            return flag
            break
    return flag

def find_successors(graph, target):
    successors = []
    task_list = list(range(0, tnum))
    for i in task_list:
            if i != target and find_edge(graph, target, i):
                successors.append(i)
    
    return successors

def find_all_ancestors(graph, target):
    ancestors = []
    task_list = list(range(0, tnum))
    for i in task_list:
            if i != target and (find_path(graph, i, target) != None):
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

# Distance between u's last successor and u.
def max_distance(task, successors, assigned_sofar):
    u = assigned_sofar.index(task)
    temp = u
    #print "u is ", u
    for t in successors:
        if assigned_sofar.index(t) > temp:
            temp = assigned_sofar.index(t)
            #print temp," for task ", t
    return temp - u


def tmb_cost(graph, assigned_sofar):
    #schedulables = find_schedulables(graph, assigned_sofar)
    tmb = 0
    #print "assigned_sofar ", assigned_sofar
    for task in assigned_sofar:
        successors = find_successors(graph, task)
        if successors == []:
            #print "Triggerred 1, no successors"
            continue
        elif set(assigned_sofar).issuperset(successors):
            tmb += max_distance(task, successors, assigned_sofar)
            #print "Triggerred 2, all successors scheduled"
        else:
            tmb += len(assigned_sofar) - assigned_sofar.index(task)
            #print "Triggerred 3"

        #print "Task ", task, " cost has been added, tmb is now ", tmb
    #print tmb
    return tmb


# Cost of the path from the start node to x. 
# In our case it's (w)tmb_cost(s).
def gx(graph, assigned_sofar, task):
    cost = 0
    assigned_sofar.append(task)
    cost = tmb_cost(graph, assigned_sofar)
    assigned_sofar.pop()
    # print cost
    return cost

# Estimation of cost of path from x to sink node.
# In our case it's the sum of outgoing edges for each task that hasn't been scheduled.
def hx(graph, assigned_sofar, task):
    cost = 0
    assigned_sofar.append(task)
    # print "s = ", assigned_sofar
    for i in range(tnum):
        if i not in assigned_sofar:
            print "cost of ", i, len(graph[i])
            cost += len(graph[i])  
    assigned_sofar.pop()
    # print "s = ", assigned_sofar
    return cost  



print gx(graph, [0,1], 4)
#print hx(graph, [0,1], 4)