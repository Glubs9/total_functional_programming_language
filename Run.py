#this file runs a string or it just builds the symbol lists.
    #it is separated into a separate file because of a circular dpeendency with Executor and Repl
        #both files call this one

from PreProcess import PreProcess
from Lexer import Lex
from Parser import Parse
from ICGenerator import Generate_IC
from Executor import Data, Execute, depth
from SemanticsChecker import Semantics_Checker

#runs a string. Execute boolean decided if this string should be run through main. (this is
    #sometimes not used when loading libraries)
def Run(str_in, execute=True):
    str_in = PreProcess(str_in)
    ast = Parse(Lex(str_in))
    ic = Generate_IC(Semantics_Checker(ast)) 
    output = Execute(ic, execute)
    return output

