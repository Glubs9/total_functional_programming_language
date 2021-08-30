#this file checks that the sum of the functions arguments depth is > the definitions depth.

from sys import exit

#entry function
def Depth_Checker(functions):
    prim_check = [n for n in functions if not check_solo(n[2])] #removes all functions that don't call other functions. e.g: f(x) = x
    arg_depth = find_arg_depth(prim_check)
    func_depth = find_func_depth(prim_check)

    #raise exception of depth of args <= depth of outputs
    for n in range(len(func_depth)):
        if arg_depth[n] <= func_depth[n]:
            print("ERROR: for function ".upper() + str(prim_check[n][1][1]) + " depth of argument data constructors is less than or equal to depth of function call data constructors".upper())
            exit()

    return functions

#any function definition where there is no other calls in the definition
def check_solo(defin):
    if type(defin) is not tuple: return True
    elif defin[0] != "data-constructor": return False
    tmp = check_solo(defin[2][0])
    return tmp

#total depth of all arguments
def find_arg_depth(functions):
    args = [n[1][2] for n in functions]
    return [sum(map(find_depth, n)) for n in args]

#depth of definition, i.e: f(x) = s[x] == 1
def find_func_depth(functions):
    return [sum(map(find_depth, find_data(n[2]))) for n in functions]

#removes extra function calls from search, i.e: f(f(s[x])) removes f
def find_data(defin):
    tmp = [n[1] for n in _find_data(defin)]
    return tmp

def _find_data(defin):
    if type(defin) is not tuple: return [(True, defin)]
    recs = list(map(_find_data, defin[2]))
    out = []
    for i in recs:
        for n in i:
            if n[0] == False: out.append(n)
            elif defin[0] != "data-constructor": out.append((False, n[1]))
            else: out.append((True, defin))
    return out

#depth of a given ast
def find_depth(f):
    if type(f) is not tuple: return 0
    return max(map(find_depth, f[2])) + 1
