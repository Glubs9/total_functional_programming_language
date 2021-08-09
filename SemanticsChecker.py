from DepthChecker import Depth_Checker
from TotalChecker import Total_Checker

def Semantics_Checker(functions):
    prim_funcs = [n for n in functions if n[1][0] == "primitive"]
    Depth_Checker(prim_funcs)
    Total_Checker(prim_funcs) #might have been better to put in the executor after analysis
    return functions
