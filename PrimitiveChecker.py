from sys import exit
from collections import defaultdict
from functools import reduce #still don't get why this isn't stdlib
from TotalChecker import group_functions

def Primitive_Checker(prim_funcs):
    """
    print("before debugging prim funcs")
    for n in prim_funcs:
        print(n)
    print("finished")
    """
    gf = group_functions(prim_funcs)
    for key, val in gf:
        if not run_checkers(val):
            print("error: function ".upper() + val[0][1][1] + " not primitive recursive".upper())
            exit()
    #run loop check / circular dependency / mutual recursion
    if not check_circular(gf):
        print("error: circular dependency detected".upper())
        exit()
    return True

def run_checkers(func_in):
    if len(func_in) == 1:
        checkers = [zero_check, succ_check, proj_check, comp_check]
        return any(map(lambda n: n(func_in[0]), checkers))
    elif len(func_in) == 2:
        return rec_check(func_in)
    else:
        print("function", func_in, "wrong number of match cases (only 1 or 2 permitted")
        exit()

#return bool
def zero_check(function):
    if not check_args(function): return False #can't successor zero function
    return function[2] == ["0"]

#this feels wrong to me
    #unary, check arg amount?
def succ_check(function):
    if type(function[2]) is not tuple: return False
    elif function[2][1] != "s": return False
    elif type(function[2][2][0][0]) is not str: return False
    return True

def proj_check(function):
    if not check_args(function): return False
    args = function[1][2]
    definition = function[2]
    if type(definition) is not list: return False
    elif len(definition) != 1: return False
    elif definition not in args: return False
    return True

#should recursively run checkers on any internal function. No I should not
def comp_check(function):

    definition = function[2]
    if type(definition) is not tuple: return False
    if not check_args(function): return False
    if definition[1] == function[1][1]: return False
    args = function[1][2]

    inner_funcs = function[2][2]
    if any(map(lambda n: type(n) is not tuple, inner_funcs)): return False
    if any(map(lambda n: n[1] == function[1][1], inner_funcs)): return False
    inner_args = [n[2] for n in inner_funcs]

    for n in inner_args:
        if not match_args(args,n):
            return False

    return True

#checks if args don't contain pattern matching
def check_args(function):
    args = function[1][2]
    return check_arg_list(args)

def check_arg_list(args):
    if args == [[]]: return True #empty arguments
    for n in args:
        if type(n) is not list: return False #arg not a variable
        elif type(n[0]) is not str: return False
    return True

def match_args(args1, args2):
    if args1 == [] and args2 == [[]]: return True #edge case i don't know why? probs symptom of bigger bug
    return sorted(args1) == sorted(args2)

#should be the easiest to write next
def rec_check(function):
    #for checking the in between functions basically I could probably just say "any function that
    #isn't the current function. this is for 0 case and the composition on the operator in the s case
    return zero_rec_check(function) and succ_rec_check(function)

def zero_rec_check(function):
    zero_funcs = [n for n in function if n[1][2][0] == ["0"]]
    if len(zero_funcs) != 1:
        print("incorrect amount of 0 match functions with function", str(function[1][1]))
        exit() #not great to exit here
    zero_func = zero_funcs[0]
    args = zero_func[1][2][1:]

    if type(zero_func[2]) is not tuple: return False
    elif not match_args(args, zero_func[2][2]): return False

    return True

#yikes this is unreadable
def succ_rec_check(function):

    succ = [n for n in function if type(n[1][2][0]) is tuple and n[1][2][0][1] == "s"]
    if len(succ) != 1: return False
    if not check_arg_list(succ[0][1][2][1:]): return False

    succ_func = succ[0]
    succ_var = succ_func[1][2][0][2][0]
    if type(succ_var) is not list: return False

    succ_var = succ_var[0]
    def_func = succ_func[2]
    if type(def_func) is not tuple: return False
    if def_func[1] == succ_func[1][1]: return False

    def_func_args = def_func[2]
    if len(def_func_args) < 2: return False
    if def_func_args[0][0] != succ_var: return False

    rec_call = def_func_args[1]
    if type(rec_call) is not tuple: return False
    if rec_call[1] != succ_func[1][1]: return False

    arg1 = rec_call[2][0]
    if arg1[0] != succ_var: return False

    if rec_call[2][1:] != succ_func[1][2][1:]: return False
    if not match_args(succ_func[1][2][1:], def_func_args[2:]): return False

    return True

#might have to recursively check the inside of each function using unary checking
#like have it so that you can check stuff that only happens inside one function and run it
#recursively
#thisi s probably needed for comp and zer oand stuff

#ok so I wasn't 100% sure on if mutual recursion is covered in primitive recursion so I just error'd
#if it is mutually recursive.
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
