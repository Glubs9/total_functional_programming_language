#this file takes in an ast and checks it to make sure it's valid.
    #it checks to make sure there is never a literal constructor on the bottom type, e.g: s[!]
    #it checks for primitive functions

from BottomChecker import Bottom_Checker
from DepthChecker import Depth_Checker
from TotalChecker import Total_Checker
from PrimitiveChecker import Primitive_Checker
from StructuralChecker import Structural_Checker

def Semantics_Checker(ast): #note, called functions don't return bools, they error the program separately
    functions = [n for n in ast if n[0] == "="] #remove the data constructors
    data = [n for n in ast if n[0] == "data"]
    Bottom_Checker(functions)
    prim_funcs = [n for n in functions if n[1][0] == "primitive"]
    #Depth_Checker(prim_funcs)
    #write depth checker thing that checks recursive functions
    Structural_Checker(prim_funcs)
    Total_Checker(prim_funcs, ast) #might have been better to put in the executor after analysis
    #Primitive_Checker(prim_funcs)
    return ast
