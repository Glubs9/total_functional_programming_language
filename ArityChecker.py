#check that you call functions with the right arities
    #including data constructors (in the arguments and also definition)
#this also builds the information for that which gets used in the executor

from functools import reduce

data_arities = {}

def get_data_arities():
    return data_arities #global keyword unecersarry

def construct_data_arities(data):
    global data_arities
    for n in reduce(lambda n1,n2: n1+n2, map(lambda n: n[2], data)): #only get constructors. Ignoring the name of the data
        if type(n) is list: #due to an oddity in the parser
            data_arities[n[0]] = 0
        elif type(n) is tuple:
            data_arities[n[1]] = len(n[2])
        else:
            raise Exception("unknown data type passed to construct data arities")

def Arity_Checker(prim_funcs, data):
    construct_data_arities(data)
    for n in prim_funcs:
        check_data_arity(n) #global data_arities used
    return True

def check_data_arity(function):
    pass
