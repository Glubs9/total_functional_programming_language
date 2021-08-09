from itertools import groupby

def Total_Checker(functions):
    gf = group_functions(functions)
    for key, val in gf:
        check_func(val)
    return functions
    
def func_name(n): 
    return n[1][1]

def group_functions(functions):
    return groupby(sorted(functions, key=func_name), func_name)

