#this file checks that there is only one data type present in the argument.

from TotalChecker import get_data_list, group_functions
from sys import exit

#this file may be expanded later but for now it just makes sure that only ever one type is usd per
#function
def Type_Checker(functions, data):
    gf = group_functions(functions)
    data_list = get_data_list()
    for key, val in gf:
        args = []
        for n in val:
            args += n[1][2]
        data_list_clone = [n for n in data_list] #data list cgetting deleted for seome reason?
        if not Check_Unique_Data_Args(args, data_list_clone):
            print("error: more than one data type found in the argument for ".upper(), functions[1][1])
            exit()
    return True

def Check_Unique_Data_Args(args, data_list):
    found = False
    for n in [i for i in data_list]:
        nia = n_in_args(n, args) #equivalent to n in args but more complicated due to data representation (stored in variable to save execution time)
        if nia and not found:
            found = True #can only find one
        elif nia and found:
            return False
        break
    else:
        print("not entered for loop with function", args, "data_list=",data_list)
    return True

def n_in_args(n, args):
    fargs = flatten_args(args)
    for i in fargs:
        if i in n: 
            return True
    return False

def flatten_args(args):
    if args == [[]]: return [] #0 arity function
    out = []
    for n in args:
        if type(n) is list: out.append(n[0]) #variables stored in one list
        elif type(n) is tuple:
            out.append(n[1])
    return out
