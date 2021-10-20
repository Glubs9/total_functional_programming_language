#this file is used to avoid circular dependency and simplify imports

from PreProcess import PreProcess
from Lexer import Lex
from Parser import Parse
from ICGenerator import Generate_IC
from Executor import Data, Execute, depth
from SemanticsCheckers.SemanticsChecker import Semantics_Checker

#runs a string. Execute boolean decided if this string should be run through main. (this is
    #sometimes not used when loading libraries)
def Run(str_in, execute=True):
    str_in = PreProcess(str_in)
    ast = Parse(Lex(str_in))
    ic = Generate_IC(Semantics_Checker(ast)) 
    output = Execute(ic, execute)
    return output

