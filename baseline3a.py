# baseline 3: some compromise or intelligent way to settle this tradeoff
# - 3a: can take jobs from later in the schedule only if they're accessing a data item already accessed in the prefix
# - 3b: if we schedule a job out-of-sequence and it uses a new data item, then recompute WTMB schedule for the suffix
# 3a is implemented.

# ADD THE CHECK for already-accessed-in-prefix

from __future__ import division
import math

print "Start process of computing multi-processor schedule with baseline 3a"

pnum = int(raw_input("Number of processors:"))
tnum = int(raw_input("Number of tasks:"))
arian = raw_input(("Input the single-thread schedule:"))

single_schedule = map(int, arian.split(' '))

print single_schedule

single_schedule_intact = list(single_schedule)

assigned_sofar = list()

delayed_index = list()
delayed = list()

pr_schedule = []

graph = {0: [21, 29, 30],
         1: [20, 21, 22, 23, 24, 25, 26, 27, 28, 30],
         2: [26, 28],
         3: [21, 26, 28, 29],
         4: [20, 22, 23, 29],
         5: [20, 21, 22, 29],
         6: [22, 29],
         7: [20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30],
         8: [29],
         9: [22, 23, 25, 26, 28],
         10: [28],
         11: [27, 30],
         12: [23, 26, 28],
         13: [23, 26, 28],
         14: [23, 26, 28],
         15: [27],
         16: [21, 27, 30],
         17: [26, 28],
         18: [24, 26, 27, 28],
         19: [26, 28]}

def pr_schedule_init(pnum, tnum):
    l = int(math.ceil(tnum / pnum))
    # print l

    for n in range(pnum):
        pr_schedule.append([None] * l)
    print(sum(x is None for x in pr_schedule[n]))
    print pr_schedule


def find_edge(graph, start, end):
    # path = path + [start]
    if start == end:
        return False
    if not graph.has_key(start):
        return False
    if end in graph[start]:
        return True
    return False


# Check if there's any edge between any assigned task and goal task.
def find_dependencies(graph, single_schedule, assigned_sofar, index):
    flag = False
    for assigned in assigned_sofar:
        if find_edge(graph, assigned, single_schedule[index]):
            flag = True
            return flag
            break
    return flag


# print find_edge(graph, 'A', 'C')
# print find_edge(graph, 'A', 'B')
# print find_edge(graph, 'E', 'D')

# Return the original index if schedulable, otherwise return the next schedulable one.
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
                    print "DEPENDENT! WILL SCHEDULE Index: ", m, " Task: ", single_schedule[m], "INSTEAD ***"
                    delayed_index.append(index)
                    delayed.append(single_schedule[index])
                    return m
                    break

        if flag:
            "DEPENDENT, BUT NO INDEPENDENT TASK CAN BE FOUND! WILL SCHEDULE IT ANYWAY ~~~"
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

def baseline3a(graph, pnum, tnum):

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
#    print delayed
    print single_schedule_intact




# pr_schedule_init(pnum, tnum)
# assign_task(pr_schedule, task)
baseline3a(graph, pnum, tnum)