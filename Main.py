from PreProcess import PreProcess
from Lexer import Lex
from Parser import Parse
from ICGenerator import Generate_IC
from Executor import Data, Execute
from SemanticsChecker import Semantics_Checker

import sys

def Run(str_in):
    str_in = PreProcess(str_in)
    tmp = Generate_IC(Semantics_Checker(Parse(Lex(str_in))))
    #supress execute output
    tmp2 = Execute(tmp)
    return tmp2

def depth(inp):
    if inp.name == "0": return 0
    else: return max(map(lambda n: n+1, map(depth, inp.data)))

test_str = open("test.tfpl", "r").read()
print(test_str + "\n")
out = Run(test_str)
print("and the output of running main is: ")
print(out)
print(depth(out))
