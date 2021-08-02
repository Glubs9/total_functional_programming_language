#jeezus this file is a mess

from sys import exit

#just checks that primitive functions are primitive
def Semantics_Checker(functions):
    #if functions are primitive recursive definitions
    prim = [n for n in functions if n[1][0] == "primitive"]
    prim_check = [n for n in prim if not check_solo(n[2])]
    #find depth of arguments
    arg_depth = find_arg_depth(prim_check)
    #find depth of outputs in function calls
    func_depth = find_func_depth(prim_check)

    #raise exception of depth of args <= depth of outputs
    for n in range(len(func_depth)):
        if arg_depth[n] <= func_depth[n]:
            print("ERROR: for function ".upper() + str(prim_check[n][1][1]) + " depth of argument data constructors is less than or equal to depth of function call data constructors".upper())
            exit()

    #check for totality
    return functions

#any function definition 
def check_solo(defin):
    if type(defin) is not tuple: return True
    elif defin[0] != "data-constructor": return False
    tmp = check_solo(defin[2][0])
    return tmp

def find_arg_depth(functions):
    args = [n[1][2] for n in functions]
    return [sum(map(find_depth, n)) for n in args]

def find_func_depth(functions):
    return [sum(map(find_depth, find_data(n[2]))) for n in functions]

def find_data(defin):
    tmp = [n[1] for n in _find_data(defin)]
    return tmp

#specifically this function is a mess
    #it recurses through trying to capture the final data depth before a function call.
def _find_data(defin):
    if type(defin) is not tuple: return [(True, defin)]
    recs = list(map(_find_data, defin[2]))
    out = []
    for i in recs: #this is a bit of a mess
        for n in i:
            if n[0] == False: out.append(n)
            elif defin[0] != "data-constructor": out.append((False, n[1]))
            else: out.append((True, defin))
    return out

def find_depth(f):
    if type(f) is not tuple: return 0
    return max(map(find_depth, f[2])) + 1
