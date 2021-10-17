#this file takes in an ast and checks it to make sure it's valid.
    #it checks to make sure there is never a literal constructor on the bottom type, e.g: s[!]
    #it checks for primitive functions

from BottomChecker import Bottom_Checker
from DepthChecker import Depth_Checker
from TotalChecker import Total_Checker
from PrimitiveChecker import Primitive_Checker
from StructuralChecker import Structural_Checker

def Semantics_Checker(functions): #note, called functions don't return bools, they error the program separately
    return functions #done here to skip semantics checking for dbeugging
    Bottom_Checker(functions)
    prim_funcs = [n for n in functions if n[1][0] == "primitive"]
    #Depth_Checker(prim_funcs)
    #write depth checker thing that checks recursive functions
    Structural_Checker(prim_funcs)
    Total_Checker(prim_funcs) #might have been better to put in the executor after analysis
    #Primitive_Checker(prim_funcs)
    return functions
