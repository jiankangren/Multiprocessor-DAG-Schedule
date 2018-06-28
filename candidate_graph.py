graph = {0: [4, 8],
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

starts = []
tnum = 22

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
        if i != target and (find_path(graph, i, target) != None):
            ancestors.append(i)

    return ancestors

def check_schedulable(graph, assigned_sofar, task):
    if set(assigned_sofar).issuperset(find_all_ancestors(graph, task)):
        return True
    else:
        return False

def find_schedulables(graph, assigned_sofar):
    schedulables = []
    for task in range(tnum):
        if (task not in assigned_sofar) and check_schedulable(graph, assigned_sofar, task):
            schedulables.append(task)

    return schedulables





def all_roots(graph):
    roots = []
    for i in range(tnum):
        if not find_all_ancestors(graph, i):
            roots.append(i)
    #print roots
    return roots


def find_one_root_candidates(graph, start, end, path=[]):
        path = path + [start]

        if start == end:
            return [path]

        if not graph.has_key(start):
            return None

        paths = []
        for node in find_schedulables(graph, path):
            if node not in path:
                newpaths = find_one_root_candidates(graph, node, end, path)
                for newpath in newpaths:
                    paths.append(newpath)
                    #print newpath
        return paths


def find_all_candidates(graph, end):
    roots = all_roots(graph)
    #print "roots ", roots
    paths = []
    for root in roots:
        print root
        paths += find_one_root_candidates(graph, root, end)

    print paths
    return paths


find_all_candidates(graph, 21)


