#this file checks that the recursive call is done with a destructured version of the input arg

from sys import exit
from TotalChecker import get_args

def Structural_Checker(prim_funcs):
    #get function arguments depth
    #search function definition to find if itself is ever called.
    #find out if the argument is a data constructor and if so, what the depth is.
    #if depth >= arg_depth return False
    args = list(map(get_args, prim_funcs))
    depths = list(map(data_depth, args)) #not correct, need to iterate to get args first instead of just doing this
    for n in range(len(prim_funcs)):
        if not structure_check(prim_funcs[n][2], prim_funcs[n][1][1], depths[n]): 
            print("error: function".upper(), prim_funcs[n][1][1], "failed structural recursion check".upper())
            exit()
    return True

def data_depth(inp):
    s = 0
    for data in inp:
        if type(data) is tuple and data[0] != "data-constructor": return False #check might be unecersarry in which case data_depth becomes _data_depth
        s += _data_depth(data)
    return s

#recursive call used in data_depth, shouldn't be called by istelf
def _data_depth(data):
    if type(data) is not tuple: return 0
    else:
        return sum(list(map(_data_depth, data[2]))) + 1 #tail call recursion doesn't matter cause python

def structure_check(func, func_name, depth):
    if type(func) is not tuple: return True
    elif func[0] == "data_constructor": return True
    elif func[1] == func_name: 
        for n in func[2]:
            if type(n) is tuple and n[0] != "data-constructor": return False #maybe double chekc the chck
        return data_depth(func[2]) < depth
    else: 
        return all(map(lambda n: structure_check(n, func_name, depth), func[2]))
