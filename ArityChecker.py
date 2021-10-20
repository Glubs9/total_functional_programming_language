#check that you call functions with the right arities
    #including data constructors (in the arguments and also definition)
#this also builds the information for that which gets used in the executor

from functools import reduce
from sys import exit

data_arities = {}
function_arities = {}

def get_data_arities(): #called in executor. used to avoid double computation. THis technique should be used more often.
    return data_arities #global keyword unecersarry

def construct_data_arities(data):
    for n in reduce(lambda n1,n2: n1+n2, map(lambda n: n[2], data), []): #only get constructors. Ignoring the name of the data
        if type(n) is list: #due to an oddity in the parser
            if n[0] in data_arities:
                print("error: redefinition of \"".upper(), n[0], "\"")
                exit()
            data_arities[n[0]] = 0
        elif type(n) is tuple:
            if n[1] in data_arities:
                print("error: redefinition of \"".upper(), n[1], "\"")
                exit()
            data_arities[n[1]] = len(n[2])
        else:
            raise Exception("unknown data type passed to construct data arities")

def construct_function_arities(functions):
    for n in list(map(lambda n: n[1], functions)):
        if n[1] in function_arities and function_arities[n[1]] != len(n[2]): #second case not matching
            print("error: function \"".upper(), n[1], "\" has cases with different arities".upper())
            exit()
        else:
            function_arities[n[1]] = len(n[2])

#entry function
def Arity_Checker(functions, data):
    construct_data_arities(data)
    construct_function_arities(functions)
    for n in functions:
        tmp = check_arity(n) #global data_arities used
        if tmp != True:
            print("error: function \"".upper(), n[1][1], "\" calls function \"".upper(), tmp, "\" with incorrect amount of arguments")
            exit()
    return True

def check_arity(function):
    return arity_rec(function[2])

#didn't work :(
def arity_rec(func_call):
    if type(func_call) is list: return True
    am = -1
    if func_call[0] == "data-constructor":
        if func_call[1] not in data_arities:
            print("error: call to non-existent data-constructor".upper(), func_call[1])
            exit()
        am = data_arities[func_call[1]]
    else:
        if func_call[1] not in function_arities:
            print("error: call to non-existent function".upper(), func_call[1])
            exit()
        am = function_arities[func_call[1]]
    if len(func_call[2]) != am: #check if 0 constructors follow this law
        return func_call[1]
    for n in func_call[2]:
        tmp = arity_rec(n)
        if tmp != True:
            return tmp
    return True
