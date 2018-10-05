from __future__ import division
import math
import time
import copy


print "Start process of computing multi-processor schedule with heuristic 5"

#pnum = int(raw_input("Number of processors:"))
tnum = int(raw_input("Number of tasks:"))
#arian = raw_input(("Enter the starting single-thread schedule:"))
#single_schedule = map(int, arian.split(' '))

#print single_schedule

#single_schedule_intact = list(single_schedule)

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
test1 = {0: [1,3,5],
     1: [],
     2: [],
     3: [],
     4: [],
     5: []}

test2 = {0: [3],
     1: [4, 2],
     2: [5, 3],
     3: [],
     4: [],
     5: []}

weight = {0: 1,
          1: 1,
          2: 1,
          3: 1,
          4: 1,
          5: 1}

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



##########################################

def find_parents(graph, target):
    parents = []
    task_list = list(range(0, tnum))
    for i in task_list:
            if i != target and (find_edge(graph, i, target) == True):
                parents.append(i)

    return parents

# Check if two tasks share a data item. If so, return the items shared.
def find_shared_data(graph, task_assigned, task_to_assign):
    set_tts =  set(find_parents(graph, task_to_assign))
    set_ta = set(find_parents(graph, task_assigned))
    results = []
    if task_assigned in find_parents(graph, task_to_assign):
        results.append(task_assigned)
    if task_assigned == task_to_assign:
        print "No shared data, start == end!!"
        return set(results)
    if (len(set_tts) == 0) or (len(set_ta) == 0):
        #print "No shared data, some task has no parents!!"
        return set(results)
    elif set_tts == set_ta:
        return set_tts
    else:
        results = set_tts.intersection(set_ta)
        return set(results)


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

def dba_cost(graph, assigned_sofar):
    #schedulables = find_schedulables(graph, assigned_sofar)
    dba = 0
    #print "assigned_sofar ", assigned_sofar

    for i in range(len(assigned_sofar)):
        for j in range(i):
            temp = 0
            shared = find_shared_data(graph, assigned_sofar[j], assigned_sofar[i])

            if len(shared) == 0:
                print "Trigger 1, no shared for ", j, " to ", i
                continue
            else:
                for item in shared:
                    data = None
                    if temp < weight[item] * (i - j - 1):
                        temp = weight[item] * (i - j - 1)
                        print "Trigger 2, cost for data item ", item, " is ", temp, " between ", j, " and ", i
                        data = item
                flag = False
                for k in range(j+1, i):
                    if data in find_shared_data(graph, assigned_sofar[k], assigned_sofar[i]):
                        flag = True
                        print "But later access found! "
                if flag == False:
                    dba += temp
                    print "COST ADDED to total between ", j, " and ", i

    return dba


#print find_parents(test1, 5)
#print find_shared_data(test1, 0, 1)
print dba_cost(test1, [0,1,2,3,4,5])