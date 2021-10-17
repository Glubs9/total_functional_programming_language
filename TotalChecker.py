#checks that a function covers all possible inputs
    #this is done recursively and is fairly complicated. 
#this is not currently used and has been repalced by primitivechecker.py
#i have kept this here because I might need it later and I put a lot of work into it so I am proud
#of it.

from itertools import groupby
from sys import exit
from collections import defaultdict

#entry funciton
def Total_Checker(functions, data):
    gf = group_functions(functions) #groups functions by function name
    data_list = [build_data_list(n[2]) for n in data]
    for key, val in gf:
        if not check_func(list(val), data_list):
            print("error: function \"".upper() + str(key) + "\" is not total".upper())
            exit()
    return functions

def build_data_list(data):
    return [n[1] if type(n) is tuple else n[0] for n in data]
    
#groups functions by function name
def group_functions(functions):
    return total_group(lambda n: n[1][1], functions)

#generic grouping function. Equivalent to groupby(sorted) except that it works for non-comparable items
def total_group(function, iterable):
    dic = defaultdict(list)
    for n in iterable:
        dic[str(function(n))].append(n)
    return dic.items()

#function to make getting args from a function tuple more readable
def get_args(function):
    return function[1][2]

#check arity of functions are all the same
    #and converts all generic args (a, b, x,..) to be called "generic" to make coding easier and more readable later on
        #note: this should be moved out of this function at a later date
def check_func(functions, data_list):
    args = list(map(get_args, functions))
    if args == [[[]]]: return True #function with no args being passed is always true
    args = list(map(lambda n: list(map(lambda i: generic_def(i, data_list), n)), args)) #converts all generic args to the same symbol
    return check_args(args, data_list) #might be able to inline

def in_data_list(string, data_list):
    for n in range(len(data_list)):
        if string in data_list[n]: return True
    return False

#converts a single function call/definition to have generic arguments
def generic_def(arg, data_list):
    if type(arg) is tuple:
        return (arg[0], arg[1], list(map(lambda n: generic_def(n, data_list), arg[2])))
    elif type(arg) is list and len(arg) == 0: return arg
    if type(arg) is list and in_data_list(arg[0], data_list):
        return arg
    elif type(arg) is list and type(arg[0]) is str:
        return ["generic"] #convert to generic
    else:
        raise Exception("totality checker generic def encountered unknown case")

#main function that checks the arguments are total
def check_args(args, data_list):
    if len(args) == 0: raise Exception("error: empty args passed to check args function".upper())
    elif len(args[0]) == 0: return True #no arguments (might end up being an error, not tested)

    #check first arg
    first_args = list(map(lambda n: n[0], args))
    if not check_arg(first_args): return False
    if len(args[0]) == 1: return True

    args = list(map(lambda n: list(n[1]), total_group(lambda n: n[0], args)))
    #recurse on each subset of matched definition
    #if that is false return false
    for i in args:
        next_args = list(map(lambda n: n[1:], i))
        if not check_args(next_args, data_list): return False
    return True

#checks a single argument list
    #note: get_args_with_name defined later
def check_arg(arg):
    if len(arg) == 0: return True #empty function is total
    if len(get_args_with_name(arg, "generic")) != 0: return True #generic arg exists
    #

    zeros = get_args_with_name(arg, "0")
    if len(zeros) == 0: return False #no zeros
    elif len(zeros) == len(arg): return False #only zero cases
    non_zeros = filter(lambda n: type(n) is tuple, arg) #similar to get args with name but with tuples
    non_zeros_less = list(map(lambda n: n[2][0], non_zeros)) #destructs the successor tuple
    if check_arg(non_zeros_less): return True
    return False #maybe raise exception

def get_args_with_name(arg, name):
    return list(filter(lambda n: n[0]==name, arg)) #[0] as args are lists
