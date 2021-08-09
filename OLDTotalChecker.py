#this total checker is wrong
    #FUCK ME have to try again

from itertools import groupby

def Total_Checker(functions):
    #group functions
    #generate combinations, test each to exist in each function
    #note: i should probably not be grouping twice (once here once in execute) in my code and I will change it later.
    #note: filter out functions that have more than one depth in the input. (or maybe like run combinations again recursively)

    #we are having issues describging totality. Please read about how other lagnuages do it. 
        #actually if we define each case then it makes sen. as in we have to have one function that is 0 and another that is s[a].
        #and all combinations of the following. Anytime we want to do more successors than we can do pred
        #this works for me
    """
    for key, val in group_functions(functions):
        if match_all([n[1][2] for n in val]) == False:
            print("error: for function ".upper() + str(key) + " function is non-total".upper())
    """

    gf = group_functions(functions)
    for key, val in gf:
        solve_one_arg(val)
    
    #ok so every stage we either have a variable we finish if we have not a variable then we need
    #both 0 and s[rec]

def func_name(n): 
    return n[1][1]

def group_functions(functions):
    return groupby(sorted(functions, key=func_name), func_name)

def solve_one_arg(functions):
    #get first args
    args = [n[1][2] for n in functions]
    if len(args[0]) != 1: return True #not checking it yet
    args = [n[0] for n in args]
    print("in solve on arg")
    for n in args:
        print(n)
    return solve_one_arg_rec(args)

def solve_one_arg_rec(args):
    if len(args) > 2: return False #only have two cases in successor case
    elif len(args) == 1 and args[0][0] == "0": return False
    elif len(args) == 1: return True
    elif len(args) == 2:
        0case = False
        if args[0][0] == "0": 0case = True
        elif args[0][0] == "0": 0case = True
        if 0case == False: return False
        scase = None
        if args[0][1] == "s": 
            scase = args[0][2]
    else:
        raise Exception("len 0 list passed to solve_one_arg_rec")

"""
def match_func(arguments, sym):
    print("match func called with " + str(arguments))
    out = []
    for n in arguments:
        if type(n[0]) is not tuple:
            if n[0] == sym: out.append(n)
        elif n[0][1] == sym: out.append(n)
    return out

def match_all(arguments):
    print("match_all called with " + str(arguments))
    if arguments == []: return True
    zeros = match_func(arguments, "0")
    if zeros == []: return False
    elif any(match_all([n[1:] for n in zeros])) == False: return False
    successors = match_func(arguments, "s")
    if successors == []: return False
    elif any(match_all([n[1:] for n in zeros])) == False: return False
    return True
"""
