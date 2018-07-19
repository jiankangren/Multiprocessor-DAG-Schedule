# h9: get an starting schedule from a* first, then assign the tasks in an online fashion:
# generate several complete schedule for each schedulable task with shotgun method,
# and choose the one with the lowest cost.

from __future__ import division
import math
import time
import copy
import random

print "Start process of computing multi-processor schedule with heuristic 9"

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
graph = {0: [7, 11],
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
      5: [8, 9, 11, 7, 10, 12, 13],
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
d3 = {0: [4, 8],
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

# SIPHT i.e. dag4.
d4 = {0: [12],
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
test = {0: [3],
        1: [4, 2],
        2: [5, 3],
        3: [],
        4: [],
        5: []}

weight = {0: 2.92,
          1: 0.225,
          2: 5.623,
          3: 0.011,
          4: 4.039,
          5: 0.054,
          6: 0.001,
          7: 0.001,
          8: 0.001,
          9: 0.001,
          10: 0.001,
          11: 0.001,
          12: 0.001,
          13: 0.001}

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
# def find_edge(graph, start, end):
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
def find_path(graph, start, end, path=[]):
    path = path + [start]
    if start == end:
        return path
    if not graph.has_key(start):
        return None
    else:
        for node in graph[start]:
            if node not in path:
                newpath = find_path(graph, node, end, path)
            if newpath:
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
    # print "u is ", u
    for t in successors:
        if assigned_sofar.index(t) > temp:
            temp = assigned_sofar.index(t)
            # print temp," for task ", t
    return temp - u


def tmb_cost(graph, assigned_sofar):
    # schedulables = find_schedulables(graph, assigned_sofar)
    tmb = 0
    # print "assigned_sofar ", assigned_sofar
    for task in assigned_sofar:
        successors = find_successors(graph, task)
        if successors == []:
            # print "Triggerred 1, no successors"
            continue
        elif set(assigned_sofar).issuperset(successors):
            tmb += weight[task] * max_distance(task, successors, assigned_sofar)
            # print "Triggerred 2, all successors scheduled"
        else:
            tmb += weight[task] * (len(assigned_sofar) - assigned_sofar.index(task))
            # print "Triggerred 3"

            # print "Task ", task, " cost has been added, tmb is now ", tmb
    # print tmb
    return tmb


def find_all_paths(graph, start, end, path=[]):
    path = path + [start]
    if start == end:
        return [path]
    if not graph.has_key(start):
        return None
    paths = []
    for node in graph[start]:
        if node not in path:
            newpaths = find_all_paths(graph, node, end, path)
            for newpath in newpaths:
                paths.append(newpath)
    return paths


def get_depth_of_node(graph, node):
    ancestors = find_all_ancestors(graph, node)
    depth = -1
    furthest = -666
    if not ancestors:

        # print "NODE ", node, " is a root, so depth is ", 0
        return 0

    else:
        for anc in ancestors:
            distance = -1
            paths = find_all_paths(graph, anc, node)
            for path in paths:
                if len(path) > distance:
                    distance = len(path)
            # print "distance is ", distance, " for ", anc, " to ", node
            if distance > depth:
                depth = distance
                furthest = anc

    # print "DEPTH of ", node, " IS ", depth
    return depth


# Find the DFS schedule for assigned_sofar partial schedule.
def dfs_schedule(graph, assigned_sofar):
    # schedulables = find_schedulables(graph, assigned_sofar)
    dfs = copy.copy(assigned_sofar)
    furthest = -666
    depth = -1
    # print "assigned_sofar ", assigned_sofar
    while len(dfs) != tnum:
        schedulables = find_schedulables(graph, dfs)
        # print "Schedulables for ", dfs, " are ", schedulables
        for task in schedulables:
            temp = get_depth_of_node(graph, task)
            if temp > depth:
                depth = temp
                furthest = task

        # print "Next to schedule: ", furthest, " with depth of ", depth

        dfs.append(furthest)
        depth = -1
        furthest = -666
    return dfs

def find_a_schedule(graph, assigned_sofar):
    schedule = copy.copy(assigned_sofar)
    while len(schedule) != tnum:
        schedulables = find_schedulables(graph, schedule)
        task = random.choice(schedulables)
        schedule.append(task)

    return schedule



# Find multiple schedules for assigned_sofar partial schedule, including the DFS.
# Default is 10.
def shotgun_schedules(graph, assigned_sofar):
    schedules = []
    dfs = dfs_schedule(graph, assigned_sofar)
    schedules.append(dfs)

    for i in range(9):
        schedule = find_a_schedule(graph, assigned_sofar)
        print "Schedule appended! "
        schedules.append(schedule)

    return schedules


def best_of_shotgun(graph, assigned_sofar):
    schedules = shotgun_schedules(graph, assigned_sofar)
    best = copy.copy(schedules[0])
    tmb = tmb_cost(graph, best)
    for schedule in schedules:
        if tmb_cost(graph, schedule) < tmb:
            best = copy.copy(schedule)

    return best


# Find the next schedulable in a greedy way.
def find_next_schedulable(graph, assigned_sofar, to_remove):
    flag = True
    all_schedulables = find_schedulables(graph, assigned_sofar)
    # print "all_schedulables in find_next_sch: ", all_schedulables
    # need to remove all the assigned tasks from all schedulables.
    schedulables = [x for x in all_schedulables if x not in to_remove]
    print "schedulables ", schedulables
    # Greedy.
    # init = assigned_sofar
    # init.append(schedulables[0])
    # print " init ", init
    # cost = tmb_cost(graph, init)

    cost = 100000000
    if not schedulables:
        print "No more schedulable task at this time... :( "
        return 88888
    else:
        fav = schedulables[0]
        # print "init cost: ", cost
        for task in schedulables:
            assigned_sofar.append(task)
            best_schedule = best_of_shotgun(graph, assigned_sofar)
            new_cost = tmb_cost(graph, best_schedule) - tmb_cost(graph, assigned_sofar)
            if new_cost < cost:
                cost = new_cost
                fav = task
                print "new best cost ", cost, " for task ", task
            assigned_sofar.pop()
            # print "The best: ", fav
    return fav


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
    # print index
    pr_schedule[processor][index] = task
    print "Task ", task, "assigned to processor ", processor, " at slot ", index


def assign_task_to_core(pr_schedule, task, core):
    processor = core
    index = pr_schedule[processor].index(next(slot for slot in pr_schedule[processor] if slot is None))
    # print index
    pr_schedule[processor][index] = task
    print "Task ", task, "assigned to processor ", processor, " at slot ", index


# As job runs, inform this program whenever a task is finished and a processor becomes idle.
# A task will be returned to be run on this idle processor.
# If this task is out of order, then the program will re-compute the schedule for remaining tasks.
# Break the loop with 66666 when the DAG is completed.
# Assume all the first 4 tasks have been assigned.

# Count of assigned tasks.

if __name__ == "__main__":

    pr_schedule_init(pnum, tnum)
    index = 0
    count = 0

    while count < tnum:
        # Initially populate the processors with one task each, i.e. the first 4 task assignment.
        if index < 4:
            start_time = time.time()
            print "Starting phase - first 4 tasks "
            print "To be scheduled is: ", single_schedule[index]
            assign_task(pr_schedule, single_schedule[index])
            assigned_sofar.append(single_schedule[index])
            print single_schedule[index], " is successfully scheduled!\n"
            single_schedule[index] = None
            # if index == 3:
            #   finished_sofar = copy.copy(assigned_sofar)
            index += 1
            count += 1
            print("--- %s seconds ---" % (time.time() - start_time))

        else:
            if count >= tnum:
                print "All tasks scheduled! Job scheduling completed. "
                break

            newDoneTask, newIdleCore = input("Task # completed on processor # split by a comma: ")

            if newDoneTask == 66666:
                print "All tasks scheduled! Job scheduling completed. "
                break

            else:
                start_time = time.time()
                finished_sofar.append(newDoneTask)
                print "finished_sofar: ", finished_sofar, " assigned_sofar: ", assigned_sofar
                todo = find_next_schedulable(graph, finished_sofar, assigned_sofar)
                if todo != 88888:
                    print "The next todo is: ", todo
                    assign_task(pr_schedule, todo)
                    assigned_sofar.append(todo)
                    print todo, " is successfully scheduled!\n"
                    # single_schedule[single_schedule.index(to do)] = None
                    count += 1
                    print("--- %s seconds ---" % (time.time() - start_time))
                else:
                    print "No more schedulable task atm, wait for another task to finish! "
                    continue

    print pr_schedule
    print single_schedule
    #   print delayed
    print single_schedule_intact

