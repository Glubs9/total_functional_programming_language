from collections import defaultdict

global_scope = defaultdict(lambda: [])

def define_functions(IC):
    for n in IC: global_scope[n[1][-1][1]].append((n[1], n[2]))

stack = [] #i'm not too happy with stack being a global variable but I will change it later

stdlib = {"$": None}
def call_stdlib(func_name, arguments):
    #raise Exception("stdlib call not implemented yet")
    stack.append((func_name, arguments)) #placeholder for debugging

#have to match the correct case and return the right function
def match_function(func_name, arguments):
    #check for empty function call
    #iterate through function definitions until correct case found
    definitions = global_scope[func_name]
    if len(definitions) == 1 and len(definitions[0]) == 1 and len(arguments) == 1: #no arguments
    #THIS IS WHERE I WAS WORKING

def call_user_defined_func(func_name, arguments):
    function = match_function(func_name, arguments)
    scope = pass_args(function[0], arguments)
    for n in function[1]:
        stack.append((scope, n))

#function written below above to aid readability
def pass_args(argument_definition, arguments):
    return []

def call_func(func_name, arguments): #although this function is simple, writing any more would be a violation of single function single responsibility
    if func_name in stdlib: call_stdlib(func_name, arguments)
    else: call_user_defined_func(func_name, arguments)

def Execute(IC):
    define_functions(IC)
    call_func("main", [])
