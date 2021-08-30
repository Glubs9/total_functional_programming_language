#this file takes in an ast and checks it to make sure it's valid.
    #it checks to make sure there is never a literal constructor on the bottom type, e.g: s[!]
    #it checks for primitive functions

from Bottom_Checker import Bottom_Checker
from DepthChecker import Depth_Checker
from TotalChecker import Total_Checker

def Semantics_Checker(functions): #note, called functions don't return bools, they error the program separately
    Bottom_Checker(functions)
    prim_funcs = [n for n in functions if n[1][0] == "primitive"]
    Depth_Checker(prim_funcs)
    Total_Checker(prim_funcs) #might have been better to put in the executor after analysis
    return functions
