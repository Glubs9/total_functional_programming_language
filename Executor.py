from collections import defaultdict

global_scope = defaultdict(lambda: [])

def construct_args(args_in):
    args = []
    for n in args_in[:-1]:
        if type(n) is not tuple: args.append(n)
        elif n[0] != "data-constructor": raise Exception("non data constructor in argument definition")
        else: args.append((n[0], n[1], args.pop())) #change to handle multi arg constructors
    return args

def define_functions(IC):
    for n in IC: 
        global_scope[n[1][-1][1]].append((construct_args(n[1]), n[2]))

call_stack = [] #i'm not too happy with stack being a global variable but I will change it later
data_stack = []

stdlib = {"s": None}
def call_stdlib(func_name):
    #raise Exception("stdlib call not implemented yet")
    call_stack.append((func_name, arguments)) #placeholder for debugging

#restricted set unification (the passed arguments must be literals)
    #hadcoded for now but will be fixed later
    #args is fully constructed at this point
    #check for successful unification
def unify(definition, args):
    if definition == [] and args == []: return []
    out = []
    for n in definition: #could zip to ensure one loop
        tmp = unify_single(n, args.pop())
        if not tmp: continue
        out.append(tmp)
    if out == []: return False
    return out

#not pure
def unify_single(definition, arg):
    if type(definition) is not list or type(definition) is not tuple: return (definition, arg)
    raise Exception("not implemented yet")

#have to match the correct case and return the right function
def match_function(func_name, arguments):
    #check for empty function call
    #iterate through function definitions until correct case found
    definitions = global_scope[func_name]
    if len(definitions) == 1 and len(definitions[0][0]) == 1: #no arguments (maybe check argument length)
        return [], definitions[0]
    for n in definitions:
        tmp = unify(n[0], arguments)
        if tmp != False: return tmp, n[0]
    print("no matching function found")

def arg_count(func_name):
    arguments = global_scope[func_name][0][0] #assuming all function definitions have the same am of args (check later)
    return len(arguments)

def call_user_defined_func(func_name):
    arguments = []
    for n in range(arg_count(func_name)):
        arguments.append(data_stack.pop())
    scope, function = match_function(func_name, arguments) #can we do this?
    for n in function[1]:
        call_stack.append((scope, n))

def call_func(func_name): #although this function is simple, writing any more would be a violation of single function single responsibility
    if func_name in stdlib: call_stdlib(func_name)
    else: call_user_defined_func(func_name)

def run():
    while (call_stack != []):
        call_func(call_stack.pop())

def Execute(IC):
    define_functions(IC)
    call_func("main")
    run()
    print("call stack")
    for n in call_stack:
        print(n)
    print("data stack")
    for n in data_stack:
        print(n)
    print()
    print(global_scope["plus"])
