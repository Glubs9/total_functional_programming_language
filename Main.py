from Lexer import Lex
from Parser import Parse
from ICGenerator import Generate_IC
from Executor import Data, Execute

def Run(str_in):
    tmp = Generate_IC(Parse(Lex(str_in)))
    return Execute(tmp)

def depth(inp):
    if inp.name == "0": return 1
    else: return max(map(lambda n: n+1, map(depth, inp.data)))

test_str = open("test.tfpl", "r").read()
print(test_str + "\n")
out = Run(test_str)
print(out)
print(depth(out))
