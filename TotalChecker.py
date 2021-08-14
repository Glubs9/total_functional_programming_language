

from itertools import groupby
from sys import exit
from collections import defaultdict

def Total_Checker(functions):
    gf = group_functions(functions)
    for key, val in gf:
        if not check_func(list(val)):
            print("error: function \"".upper() + str(key) + "\" is not total".upper())
            exit()
    return functions
    
def group_functions(functions):
    return total_group(lambda n: n[1][1], functions)

def total_group(function, iterable):
    #we re-write group here instead of using below because sorting is not possible on all structures
    #return groupby(sorted(iterable, key=function), function)
    dic = defaultdict(list)
    for n in iterable:
        dic[str(function(n))].append(n)
    return dic.items()

def get_args(function):
    return function[1][2]

def check_func(functions):
    #check arity of functions are all the same
    args = list(map(get_args, functions))
    args = list(map(lambda n: list(map(generic_def, n)), args)) #converts all generic args to the same symbol
    return check_args(args) #might be able to inline

def generic_def(arg):
    if type(arg) is tuple:
        return (arg[0], arg[1], [generic_def(arg[2][0])]) #successor
    elif type(arg) is list and arg[0] == "0":
        return ["0"]
    elif type(arg) is list and type(arg[0]) is str:
        return ["generic"] #convert to generic
    else:
        raise Exception("totality checker generic def encountered unknown case")

def check_args(args):
    if len(args) == 0: raise Exception("error: empty args passed to check args function".upper())
    elif len(args[0]) == 0: return True #no arguments (might end up being the above)

    #check first arg
    first_args = list(map(lambda n: n[0], args))
    if not check_arg(first_args): return False
    if len(args[0]) == 1: return True

    args = list(map(lambda n: list(n[1]), total_group(lambda n: n[0], args)))
    #recurse on each subset of matched definition
    #if that is false return false
    for i in args:
        next_args = list(map(lambda n: n[1:], i))
        if not check_args(next_args): return False
    return True

def check_arg(arg):
    if len(arg) == 0: return True #empty function is total?
    if len(get_args_with_name(arg, "generic")) != 0: return True
    zeros = get_args_with_name(arg, "0")
    if len(zeros) == 0: return False
    elif len(zeros) == len(arg): return False #only zero cases
    non_zeros = filter(lambda n: type(n) is tuple, arg) #similar to get args with name but with tuples
    non_zeros_less = list(map(lambda n: n[2][0], non_zeros))
    if check_arg(non_zeros_less): return True
    return False #maybe raise exception

def get_args_with_name(arg, name):
    return list(filter(lambda n: n[0]==name, arg)) #[0] as args are lists
