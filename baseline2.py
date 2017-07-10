# - baseline 2: to improve CPU utilization, take jobs from later in the schedule and run them earlier
# (go as far as you want, so focus on cpu utilization at the cost of breaking locality)


from __future__ import division
import math

print "Start process of computing multi-processor schedule with baseline 2"

pnum = int(raw_input("Number of processors:"))
tnum = int(raw_input("Number of tasks:"))
arian = raw_input(("Input the single-thread schedule:"))

single_schedule = map(int, arian.split(' '))
print single_schedule
pr_schedule = []

graph = { 0: [7, 11],
          1: [11],
          2: [8, 9],
          3: [8, 9, 11, 7, 10, 12, 13],
          4: [10, 12, 13],
          5: [8, 9, 11, 7, 10 ,12, 13],
          6: [8, 9, 11],
          7: [],
          8: [],
          9: [],
          10: [],
          11: [],
          12: [],
          13: []}


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


# Check if there's any edge between any task (from start to end) and end task.
def find_dependencies(graph, start, end):
    flag = False
    for n in range(start, end):
        if find_edge(graph, n, end):
            flag = True
            return flag
            break
        else:
            flag = False
    return flag


# print find_edge(graph, 'A', 'C')
# print find_edge(graph, 'A', 'B')
# print find_edge(graph, 'E', 'D')

# Return the original index if schedulable, otherwise return the next schedulable one.
def find_next_schedulable(graph, single_schedule, index):
    flag = True

    if not find_dependencies(graph, 0, index):
        return index
    elif index+1 <= tnum and find_dependencies(graph, 0, index):
        find_next_schedulable(graph, single_schedule, index+1)
    else:
        return index



# Always find the schedule with most empty slots; break ties arbitrarily.
def find_processor(pr_schedule):
    max = 0
    processor = -1
    for item in pr_schedule:
        tmp = sum(x is None for x in item)
        if tmp > max:
            max = tmp
            processor = pr_schedule.index(item)
    if processor == -1:
        print "No slot available now!"
        return
    else:
        return processor


def assign_task(pr_schedule, task):
    processor = find_processor(pr_schedule)
    index = pr_schedule[processor].index(next(slot for slot in pr_schedule[processor] if slot is None))
    print index
    pr_schedule[processor][index] = task
    print "Task ", task, "assigned to processor ", processor, " at slot ", index

def baseline2(graph, pnum, tnum):

    pr_schedule_init(pnum, tnum)

    index = 0

    while single_schedule != [None]*tnum:
        print "Now scheduling ", single_schedule[index]

        for n in range(tnum):
            if single_schedule[m] != None:
                assign_task(pr_schedule, single_schedule[n])
                single_schedule[index] = None


    print pr_schedule




# pr_schedule_init(pnum, tnum)
# assign_task(pr_schedule, task)
baseline1(graph, pnum, tnum)