#checks for mutual recursion in primitive functions
    #and errors if discovered

from TotalChecker import group_functions
from collections import defaultdict
from functools import reduce
from sys import exit

def Circular_Checker(functions):
    gf = group_functions(functions)
    if not check_circular(gf):
        print("error: circular dependency detected".upper())
        exit()
    return True

def check_circular(grouped_functions):
    #build adjacency matrix
    graph = defaultdict(lambda: set())
    for key,val in grouped_functions:
        for f in val:
            func_name = f[1][1]
            for n in called_functions(f[2]):
                if n != func_name: graph[func_name].add(n) #filter out func name probs
    return graph_circular_check(graph)

def called_functions(function):
    if type(function) is list: return [] #list means variable so now good
    elif type(function) is tuple:
        add_name = function[1] #might filter out successor 4 the gainzzz (speed optimization), probs not tho lol
        return [add_name] + reduce(lambda n1,n2: n1+n2, map(called_functions, function[2])) #not fast, change later?
    else:
        raise Exception("interpreter error, unknown case reached in called_functions with: " + str(function))

def graph_circular_check(graph):
    return not any((circular_check_rec(graph, k) for k,v in graph.items())) #slow as hek but will do for now since i'm rushing a bitlol (have to iterate through all cause graph isn't fully conectedded)

def circular_check_rec(graph, name, prev=set()):
    if name not in graph: return False #recursing with like inbuilt stdlib func
    for n in graph[name]:
        if n in prev: return True
        send_prev = prev.copy()
        send_prev.add(n)

        tmp = circular_check_rec(graph, n, send_prev)
        if tmp: return True
    return False
