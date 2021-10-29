#checks that a function covers all possible inputs
    #this is done recursively and is fairly complicated. 

from itertools import groupby
from sys import exit
import ast
from collections import defaultdict

#entry funciton
def Total_Checker(functions, data):
    gf = group_functions(functions) #groups functions by function name
    [build_data_list(n[2]) for n in data]
    data_list = get_data_list()
    for key, val in gf:
        if not check_func(list(val), data_list):
            print("error: function \"".upper() + str(key) + "\" is not total".upper())
            exit()
    return functions

memo = set() #data list brings in many files. need to add to data list every time
def build_data_list(data):
    global memo
    memo.add(str([n[1] if type(n) is tuple else n[0] for n in data])) #str cause list unhasable
    return None #shouldn't be used to get data. use get_data_list to get data

def get_data_list():
    global memo
    return list(map(ast.literal_eval, memo)) #bit slow and bit yikes
    
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
    if not check_arg(first_args, data_list): return False
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
    #only checks one type. multitype function not currently supported
#this function is a little big and ugly but nothing much can be done really
    #at least it's pure (ok not technically but pure enough for me to live with)
    #i can't really comment on the logic. not enough space or time.
def check_arg(arg, data_list):
    if len(arg) == 0: return True #empty function is total
    if len(get_args_with_name(arg, "generic")) != 0: return True #generic arg exists

    #figure out what data input the arg is
    type_list = find_type(arg, data_list)

    #check that all cases are covered
    frequencies = {name: 0 for name in type_list}
    for n in arg:
        if type(n) is list and n[0] == "generic": 
            continue
        elif (n[1] if type(n) is tuple else n[0]) not in frequencies:
            return False
        frequencies[n[1] if type(n) is tuple else n[0]] += 1

    #don't check redefinition here. Multiple args means more combinations
    for key, val in frequencies.items():
        if val == 0:
            return False

    #group together similar constructors / tuples
    #call check_arg with [2] and run alll on that list

    d = defaultdict(lambda: []) #redefining grouping but it's not a big deal
    for n in arg:
        if type(n) is tuple:
            d[n[1]].append(n[2])

    #recursive call (note: the halting case is a little hidden, but it's basically when there is no tuple or all constructors are of arity 0)
    for k,v in d.items():
        for n in range(len(v[0])): #v is 2d array
            call_vals = [i[n] for i in v] #get args together. i.e: list[a,b] list[a,b] will rec call on all a's
            if check_arg(call_vals, data_list) == False: #don't really return false. Mostly just error out. Should get that fixed at some point
                return False
    return True

def find_type(arg, data_list):
    arg1 = arg[0] #we should be able to find it through only the first arg
    for n in data_list:
        if type(arg1) is list and arg1[0] in n: return n
        if type(arg1) is tuple and arg1[1] in n: return n
    raise Exception("no known type found for arg", arg1)

def get_args_with_name(arg, name):
    return list(filter(lambda n: n[0]==name, arg)) #[0] as args are lists
