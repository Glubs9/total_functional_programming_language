from PreProcess import PreProcess
from Lexer import Lex
from Parser import Parse
from ICGenerator import Generate_IC
from Executor import Data, Execute
from SemanticsChecker import Semantics_Checker
import sys

def Run(str_in, execute=True):
    str_in = PreProcess(str_in)
    tmp = Parse(Lex(str_in))
    tmp = Generate_IC(Semantics_Checker(tmp))
    tmp = Execute(tmp, execute)
    return tmp

def depth(inp):
    if inp.name == "!": return -1
    if inp.name == "0": return 0
    else: return max(map(lambda n: n+1, map(depth, inp.data)))

stdlib_str = open("stdlib.tfpl", "r").read()
Run(stdlib_str, False)

if len(sys.argv) != 2:
    print("wrong number of arguments passed / Please pass a file")
    sys.exit()
inp_file = open(sys.argv[1]).read()
out = Run(inp_file)

print("the output of running main in file " + sys.argv[1] + " is: ")
print(out)
print("with a depth of " + str(depth(out)))
