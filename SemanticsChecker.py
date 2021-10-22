#this file takes in an ast and checks it to make sure it's valid.
    #it checks to make sure there is never a literal constructor on the bottom type, e.g: s[!]
    #it checks for primitive functions

from BottomChecker import Bottom_Checker
from TotalChecker import Total_Checker
from StructuralChecker import Structural_Checker
from ArityChecker import Arity_Checker
from CircularChecker import Circular_Checker
from TypeChecker import Type_Checker
from BracketChecker import Bracket_Checker

#i feel i should be able to generalize a checker and be able to write it so that I can write less
#repeated code. probably something to do with 
def Semantics_Checker(ast): #note, called functions don't return bools, they error the program separately
    functions = [n for n in ast if n[0] == "="] #remove the data constructors
    functions = [(n[0], n[1], remove_hashtag(n[2])) for n in functions] #remove # from call
    data = [n for n in ast if n[0] == "data"]
    Bottom_Checker(functions)
    Arity_Checker(functions, data)
    Bracket_Checker(functions, data)
    prim_funcs = [n for n in functions if n[1][0] == "primitive"]
    Structural_Checker(prim_funcs)
    Total_Checker(prim_funcs, data)
    Type_Checker(prim_funcs, data)
    Circular_Checker(prim_funcs)
    return ast

def remove_hashtag(function):
    if type(function) is list: return function
    elif type(function) is tuple:
        if function[1][0] == "#":
            return (function[0], function[1][1:], list(map(remove_hashtag, function[2])))
        else:
            return (function[0], function[1], list(map(remove_hashtag, function[2])))
    else:
        raise Exception("unknown case here")

