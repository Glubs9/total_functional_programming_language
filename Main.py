from Lexer import Lex
from Parser import Parse
from ICGenerator import Generate_IC
from Executor import Execute

def Run(str_in):
    tmp = Generate_IC(Parse(Lex(str_in)))
    Execute(tmp)
    return tmp

test_str = "plus(0, b) = b; plus(s[a], b) = s[plus(a, b)]; main() = plus(s[s[s[0]]], s[s[0]]);"
print(test_str + "\n")
for n in Run(test_str):
    for i in n:
        print(i)
    print()
