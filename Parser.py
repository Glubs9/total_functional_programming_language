#this file parses lexed tokens.
    #the only issue currently with this is that I am using tuples to represent my ast.
    #I may have to change this later to a more readable and understandable format, 
    #as for now I have opted not to as this is understandable enough and it hasn't caused enough
    #problems for me to need to change this. (I understand the concept of technical debt but I have chosen to ignore it)

#entry function at the bottom of the file

def split_lines(tokens, split_str): #equivalent of .split(split_str) for a token list
    out = []
    tmp = []
    for n in tokens:
        if n == split_str: 
            out.append(tmp)
            tmp = []
        else: tmp.append(n)
    out.append(tmp)
    return out

inverse = {"(": ")", "{": "}", "[": "]"} #inverse feels a little unecersarry
open_brackets = set(inverse.keys()) 
closed_brackets = {inverse[n] for n in open_brackets}
#splits the array into arguments separated by commas, but only on the top scope
    #this is passed a funciton call i.e: asdf(1,2,3,s[4]) will be passed
def split_comma_on_top(arr):
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
def build_function(func_call): #builds a function tuple, e.g: ("primitive", [func_name] , [args])
    if len(func_call) <= 1: return func_call #it's recursive
    brack_type = brack_name[func_call[1]]
    func_name = func_call[0]
    arguments = [build_function(n) for n in split_comma_on_top(func_call)]
    return (brack_type, func_name, arguments)

import sys #only place it's used is in this function so i put it here for readability
def build_tree(li): #builds a full function definition, i.e: ["=", f(x), x] (but it would be parsed)
    print("li=",li)
    if li[0] == "data":
        tmp = ["data", li[1]]
        for n in split_lines(li[3:], "|"):
            print("found n", n)
            tmp.append(build_function(n))
        return tmp
    else:
        try:
            i = li.index("=")
        except ValueError:
            print("no equals sign found in function " + str(li))
            sys.exit()
        return ["=", build_function(li[:i]), build_function(li[i+1:])]

def Parse(tokens):
    lines = split_lines(tokens, ";")[:-1] #last line is empty
    functions = list(map(build_tree, lines))
    print("parsed")
    for n in functions:
        print(n)
    return functions
