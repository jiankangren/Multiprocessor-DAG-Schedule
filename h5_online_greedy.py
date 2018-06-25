# h5: get an starting schedule from a* first, then re-compute with that fixed prefix every time
# a task is scheduled out of order.

from __future__ import division
import math
import time

print "Start process of computing multi-processor schedule with heuristic 3"

pnum = int(raw_input("Number of processors:"))
tnum = int(raw_input("Number of tasks:"))
arian = raw_input(("Enter the starting single-thread schedule:"))
single_schedule = map(int, arian.split(' '))

print single_schedule

single_schedule_intact = list(single_schedule)

assigned_sofar = list()

delayed_index = list()
delayed = list()

pr_schedule = []

# DAG2 - Deeper 7Q
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

# Find the next schedulable in a greedy way.
def find_next_schedulable(graph, single_schedule, assigned_sofar, index):
    flag = True

    if not find_dependencies(graph, single_schedule, assigned_sofar, index):
        print "NOT DEPENDENT ON PREVIOUS TASKS, CAN BE SCHEDULED $$$"
        return index
    else:
        #if index+1 < tnum:
        #    find_next_schedulable(graph, single_schedule, index+1)
        #else:
        #    return index

        for m in range(index+1, tnum):
            if single_schedule[m] != None:
                flag = find_dependencies(graph, single_schedule, assigned_sofar, m)
                if not flag:
                    print single_schedule[index], " IS DEPENDENT, will schedule Index: ", m, " Task: ", single_schedule[m], "INSTEAD ***"
                    delayed_index.append(index)
                    delayed.append(single_schedule[index])
                    return m
                    break
                else:
                    print single_schedule[index], " is dependent, ", single_schedule[m], "is dependent too!"

        if flag:
            single_schedule[index], "IS DEPENDENT, BUT NO INDEPENDENT TASK CAN BE FOUND! WILL SCHEDULE IT ANYWAY ~~~"
            return index


# Always find the schedule with most empty slots; break ties arbitrarily.
def find_processor(pr_schedule):
    tmax = 0
    processor = -1
    for item in pr_schedule:
        tmp = sum(x is None for x in item)
        if tmp > tmax:
            tmax = tmp
            processor = pr_schedule.index(item)
    if processor == -1:
        print "No slot available now!"
        return
    else:
        return processor


def assign_task(pr_schedule, task):
    processor = find_processor(pr_schedule)
    index = pr_schedule[processor].index(next(slot for slot in pr_schedule[processor] if slot is None))
    #print index
    pr_schedule[processor][index] = task
    print "Task ", task, "assigned to processor ", processor, " at slot ", index


def assign_task_to_core(pr_schedule, task, core):
    processor = core
    index = pr_schedule[processor].index(next(slot for slot in pr_schedule[processor] if slot is None))
    #print index
    pr_schedule[processor][index] = task
    print "Task ", task, "assigned to processor ", processor, " at slot ", index

def h5(graph, pnum, tnum):

    pr_schedule_init(pnum, tnum)

    index = 0

    # while single_schedule != [None]*tnum:

    for n in range(tnum):

        print "Now scheduling ", single_schedule[n]
        if single_schedule[n] != None:
            print "Index ", n, "in schedule is not None, can be scheduled!"
            next_to_schedule = find_next_schedulable(graph, single_schedule, assigned_sofar, n)
            print "To be scheduled is index: ", next_to_schedule
            assign_task(pr_schedule, single_schedule[next_to_schedule])
            assigned_sofar.append(single_schedule[next_to_schedule])
            print single_schedule[next_to_schedule], " is successfully scheduled!\n"
            single_schedule[next_to_schedule] = None
        else:
            print "Already out-of-order scheduled!!!\n"

    if len(delayed) > 0:
        for k in delayed_index:
            print "Have to schedule DELAYED task: ", single_schedule[k]
            assign_task(pr_schedule, single_schedule[k])
            print single_schedule[k], " is (FINALLY) successfully scheduled!\n"
            single_schedule[k] = None

    print delayed
    del delayed[:]


    print pr_schedule
    print single_schedule
#   print delayed
    print single_schedule_intact



# As job runs, inform this program whenever a task is finished and a processor becomes idle.
# A task will be returned to be run on this idle processor.
# If this task is out of order, then the program will re-compute the schedule for remaining tasks.
# Break the loop with 66666 when the DAG is completed.
# Assume all the first 4 tasks have been assigned.

# Count of assigned tasks.

pr_schedule_init(pnum, tnum)
index = 0

while index < tnum:
    # Initially populate the processors with one task each, i.e. the first 4 task assignment.
    if index < 4:
        start_time = time.time()
        print "Starting phase - first 4 tasks "
        print "To be scheduled is index: " + index
        assign_task(pr_schedule, single_schedule[index])
        assigned_sofar.append(single_schedule[index])
        print single_schedule[index], " is successfully scheduled!\n"
        single_schedule[index] = None
        index += 1
        print("--- %s seconds ---" % (time.time() - start_time))

    else:
        if index >= tnum:
            print "All tasks scheduled! Job scheduling completed. "
            break

        newDoneTask, newIdleCore = int(input("Task # completed on processor # split by a comma: "))

        if newDoneTask == 66666:
            print "All tasks scheduled! Job scheduling completed. "
            break 

        else:
            start_time = time.time()
            print "To be scheduled is index: ", index
            next_to_schedule = find_next_schedulable(graph, single_schedule, assigned_sofar, index)
            if (next_to_schedule == index):
                assign_task_to_core(pr_schedule, single_schedule[next_to_schedule], newIdleCore)
                assigned_sofar.append(single_schedule[index])
                single_schedule[next_to_schedule] = None
            else: 



            index += 1
            print("--- %s seconds ---" % (time.time() - start_time))

