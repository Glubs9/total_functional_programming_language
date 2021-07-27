from Utility import bind

#this would be a lot easier with a tagged union
#i kinda wanna write it in haskell, for the fun of it. maybe do it later?
    #honestly i'm might switch. well nah cuase how do we do asynchronous stuff
    #well actually a tuple with the token at the front is a tagged union in some ways
    #parse to infix notation

#note: this parser is a bit bad?
    #I mean it is hard coded but I think that it works better that way
    #if this was written to handle a generic syntax to allow for more flexibility the output ast
    #would be worse, and also that that point I could just use a library

def split_lines(tokens):
    #could do with a reduce but i'm lazy
        #idk if .split works on lists but if it does then replace with that
    out = []
    tmp = []
    for n in tokens:
        if n == ";": 
            out.append(tmp)
            tmp = ""
        else: tmp.append(n)
    return out

inverse = {"(": ")", "{": "}", "[": "]"}
def find_matching(string, start_pos):
    open_brack = string[start_pos]
    close_brack = inverse[open_brack]
    needed = 1
    n = start_pos+1
    while n < len(string) and needed != 0:
        if string[n] == open_brack: needed+=1
        elif string[n] == close_brack: needed-=1
    return n-1

def build_functions(line):
    #split_to_function_calls
    #compress each function call
    #return list of function calls

def split_on_eq(li):
    #error check here later
    i = li.index("=")
    return ("=", li[:i], li[i+1:])

def Parse(tokens):
    lines = split_lines(tokens)
    functions = bind(build_functions, lines)
    equality = bind(split_on_eq, functions)
