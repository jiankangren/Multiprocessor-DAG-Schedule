import collections
import heapq

class PriorityQueue:
    def __init__(self):
        self.elements = []
    
    def empty(self):
        return len(self.elements) == 0
    
    def put(self, item, priority):
        heapq.heappush(self.elements, (priority, item))
    
    def get(self):
        return heapq.heappop(self.elements)[1]

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


# Here it's assumed that all tasks in assigned_sofar are finished.
# In retrospect it should be finished_sofar.
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


def cost_estimate(graph, assigned_sofar, task):
	return hx(graph, assigned_sofar, task)+gx(graph, assigned_sofar, task)


def a_star_recompute(graph, assigned_sofar, task):
	fav = []
	fav_cost = 0
    
    
    while not frontier.empty():
        current = frontier.get()
        
        if current == goal:
            break


