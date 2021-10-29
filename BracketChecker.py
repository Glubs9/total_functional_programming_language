#this files checks that the right braackets are used with the right functions

from sys import exit
from functools import reduce
from Stdlib import stdlib_types

func_type = {} #global because it needs to be stored between file loads

def detect_types(functions, data):
    it_list = reduce(lambda n1,n2: n1+n2, map(lambda n: n[2], data), []) + list(map(lambda n: n[1], functions))
    for n in it_list:
        if type(n) is list: #unit type in data constructors is the only thing that exists like this (not great code)
            if n[0] in func_type and func_type[n[0]] != "data-constructor":
                print("error: function case with non matching brackets in function ".upper(), n[0])
                exit()
            func_type[n[0]] = "data-constructor" #redefinition checked in arity_checker so don't need to check here
        elif type(n) is tuple:
            if n[1] in func_type and func_type[n[1]] != n[0]:
                print("error: function case with non matching brackets in function ".upper(), n[0])
                exit()
            func_type[n[1]] = n[0]
        else:
            raise Exception("unknown case in detect_types")
    func_type.update(stdlib_types)

def Bracket_Checker(functions, data):
    detect_types(functions, data)
    for n in functions:
        cfc = check_func_call(n[2])
        if cfc != True:
            print("error: function".upper(), cfc, "called with incorrect brackets in function".upper(), n[1][1])
            exit()
    return True

def check_func_call(func_call):
    if func_call == [[]] or func_call == []: return True #empty function args
    elif type(func_call) is list:
        if func_call[0] in func_type and func_type[func_call[0]] != "data-constructor":
            return func_call[0]
    elif type(func_call) is tuple:
        if func_call[1] not in func_type:
            raise Exception("unknown function detected in check_func_call")
        elif func_type[func_call[1]] != func_call[0]:
            return func_call[1]
        for n in map(check_func_call, func_call[2]):
            if n != True: return n
    else:
        raise Exception("unknown case detected in check_func_call in BracketChecker.py")
    return True
