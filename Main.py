from Lexer import Lex
from Parser import Parse

def Run(str_in):
    return Parse(Lex(str_in))

test_str = "plus(0, b) = b; plus(s[a], b) = s[plus(a, b)]; main() = plus(s[s[s[0]]], s[s[0]]);"
