#this is the main file, it handles io and the integration of all the modules together.
#later on it would be worth separating these, i.e: io one file and integration another, but this
#project is small enough for now that it is not necersarry

from PreProcess import PreProcess
from Lexer import Lex
from Parser import Parse
from ICGenerator import Generate_IC
from Executor import Data, Execute, depth
from SemanticsChecker import Semantics_Checker
import sys

#runs a string. Execute boolean decided if this string should be run through main. (this is
    #sometimes not used when loading libraries)
def Run(str_in, execute=True):
    str_in = PreProcess(str_in)
    ast = Parse(Lex(str_in))
    ic = Generate_IC(Semantics_Checker(ast)) 
    output = Execute(ic, execute)
    return output

stdlib_str = open("stdlib.tfpl", "r").read()
Run(stdlib_str, False) #do not execute main function

if len(sys.argv) != 2:
    print("wrong number of arguments passed / Please pass a file")
    sys.exit()
inp_file = open(sys.argv[1]).read()
out = Run(inp_file)

print("the output of running main{} in file " + sys.argv[1] + " is: ")
print(out)
print("with a depth of " + str(depth(out)))
