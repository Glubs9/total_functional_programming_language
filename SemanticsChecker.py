from Bottom_Checker import Bottom_Checker
from DepthChecker import Depth_Checker
from TotalChecker import Total_Checker

def Semantics_Checker(functions):
    #check brackets
    prim_funcs = [n for n in functions if n[1][0] == "primitive"]
    Bottom_Checker(prim_funcs)
    Depth_Checker(prim_funcs)
    Total_Checker(prim_funcs) #might have been better to put in the executor after analysis
    return functions
