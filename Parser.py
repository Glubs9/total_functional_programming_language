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

#we can change data representation later, but for now this is easy enough

def split_lines(tokens):
    #could do with a reduce but i'm lazy
        #idk if .split works on lists but if it does then replace with that
    out = []
    tmp = []
    for n in tokens:
        if n == ";": 
            out.append(tmp)
            tmp = []
        else: tmp.append(n)
    return out

inverse = {"(": ")", "{": "}", "[": "]"}
open_brackets = list(inverse.keys()) 
closed_brackets = [inverse[n] for n in open_brackets]
#splits the array into arguments separated by commas, but only on the top scope
    #this is passed a funciton call i.e: asdf(1,2,3,jkl[4]) will be passed
def split_comma_on_top(arr): #assuming balanced parenthesis have been checked
    needed = 0
    out = []
    tmp = []
    for n in range(2, len(arr)-1):
        if needed == 0 and arr[n] == ",": 
            out.append(tmp)
            tmp = []
        else:
            tmp.append(arr[n])
        if arr[n] in open_brackets: needed+=1
        elif arr[n] in closed_brackets: needed-=1
    out.append(tmp) #assuming non empty input
    return out

brack_name = {"(": "primitive", "{": "non-primitive", "[": "data-constructor"}
def build_function(func_call):
    if len(func_call) <= 1: return func_call
    #passing only one function
    brack_type = brack_name[func_call[1]]
    func_name = func_call[0]
    arguments = [build_function(n) for n in split_comma_on_top(func_call)]
    return [brack_type, func_name, *arguments]

def build_tree(li):
    #error check here later
    i = li.index("=")
    return ["=", build_function(li[:i]), build_function(li[i+1:])]

def Parse(tokens):
    lines = split_lines(tokens)
    functions = list(map(build_tree, lines))
    return functions
