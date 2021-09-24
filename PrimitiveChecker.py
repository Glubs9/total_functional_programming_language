from TotalChecker import group_functions
from sys import exit

def Primitive_Checker(prim_funcs):
    print("before debugging prim funcs")
    for n in prim_funcs:
        print(n)
    print("finished")
    gf = group_functions(prim_funcs)
    for key, val in gf:
        if not run_checkers(val):
            print("function " + val[0][1][1] + " not primitive recursive")
            exit()
    #run loop check / circular dependency / mutual recursion
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
    args = function[1][2]

    inner_funcs = function[2][2]
    if any(map(lambda n: type(n) is not tuple, inner_funcs)): return False
    print(function)
    print(inner_funcs)
    inner_args = [n[2] for n in inner_funcs]

    for n in inner_args:
        if not match_args(args, inner_args):
            return False

    return True

#checks if args don't contain pattern matching
def check_args(function):
    print(function)
    args = function[1][2]
    if args == [[]]: return True #empty arguments
    for n in args:
        if type(n) is not list: return False #arg not a variable
        elif type(n[0]) is not str: return False
    return True

def match_args(args1, args2):
    return sorted(args1) == sorted(args2)

#should be the easiest to write next
def rec_check(function):
    #for checking the in between functions basically I could probably just say "any function that
    #isn't the current function. this is for 0 case and the composition on the operator in the s case
    return True


#might have to recursively check the inside of each function using unary checking
#like have it so that you can check stuff that only happens inside one function and run it
#recursively
#thisi s probably needed for comp and zer oand stuff
