#todo:
    #chnage from tuple rpresentation to oo rep
        #cause i think a lot of the current bugs comes fomr not understanding the structure
        #it's pretty unreadable
        #screw it for now though hey?

from collections import defaultdict

global_scope = defaultdict(lambda: [])

class Function:
    def __init__(self, argments, definition): #add type signature
        self.arguments = arguments
        self.definition = definition
    def __str__(self):
        return "function: " + str(argments) + " : " + str(definition)

class Data:
    def __init__(self, name, data):
        self.name = name
        self.data = data
    def __str__(self):
        return self.name + "[" + " ,".join(map(str, self.data)) + "]"

#class Var: #i dont implement this class because it is just a tuple (maybe if readability gets bad)

def construct_args(args_in):
    args = []
    for n in reversed(args_in[1:]):
        if type(n) is not tuple: args.append(Data(n, []))
        elif n[0] != "data-constructor": raise Exception("non data constructor in argument definition")
        else: args.append(Data(n[1], [args.pop()])) #change later to handle multi arg constructors
    return args

def define_functions(IC):
    for n in IC: 
        global_scope[n[1][0][1]].append(Function((construct_args(n[1]), n[2])))

call_stack = [] #i'm not too happy with stack being a global variable but I will change it later
data_stack = []

stdlib = {
        "0": lambda: data_stack.append(Data('0', [])), 
        "s": lambda: data_stack.append(Data("s", [data_stack.pop()]))
}
def call_stdlib(func_name):
    stdlib[func_name]()

#restricted set unification (the passed arguments must be literals)
    #hadcoded for now but will be fixed later
    #args is fully constructed at this point
    #check for successful unification
#TODO: fix this
def unify(definition, args):
    if definition == [] and args == []: return []
    if len(definition) != len(args): return False
    out = []
    for n in definition: #could zip to ensure one loop
        tmp = unify_single(n, args.pop())
        if tmp == False: return False
        out += tmp
    if out == []: return False
    return out

#not pure
def unify_single(definition, arg):
    if definition.name == "0" and arg.name == "0": return []
    elif arg.name != "s": return [(definition, arg)] #check for non-snytacitcal definition
    elif definition.name == "0": return False
    else: return unify_single(definition[2], arg[2])

#have to match the correct case and return the right function
def match_function(func_name, arguments):
    #check for empty function call
    #iterate through function definitions until correct case found
    definitions = global_scope[func_name]
    if len(definitions) == 1 and len(definitions[0][0]) == 0: #no arguments (maybe check argument length)
        return [], definitions[0]
    for n in definitions:
        tmp = unify(n[0], arguments)
        if tmp != False: return tmp, n[0]
    print("no matching function found")
    raise Exception("branch not found yet")

def arg_count(func_name):
    print("getting argument count with func " + str(func_name))
    tmp = global_scope[func_name][0] #assuming all functions have same arity
    return len(tmp.arguments)

def call_user_defined_func(func_name):
    arguments = []
    for n in range(arg_count(func_name)):
        arguments.append(data_stack.pop())
    scope, function = match_function(func_name, arguments) #can we do this?
    for n in function.definition:
        call_stack.append((scope, n))

def var_in_scope(func_name, scope):
    print("testing var with sope + " + str(scope))

def call_func(func_name, scope): #although this function is simple, writing any more would be a violation of single function single responsibility
    #check for func_name in scope
    if var_in_scope(func_name, scope): handle_var(func_name, scope)
    elif func_name in stdlib: call_stdlib(func_name)
    else: call_user_defined_func(func_name)

def run():
    it = 1
    while (call_stack != []):
        print("it am = " + str(it))
        print("call_satck")
        for n in call_stack:
            print(n)
        print("data_stack")
        for n in data_stack:
            print(n)
        print("")
        tmp = call_stack.pop()
        if type(tmp[1]) is not tuple: #sometimes I push to the stack the literal name cause i'm layz, this needs to be re-written
            call_func(tmp[1], tmp[0])
        else:
            call_func(tmp[1][1], tmp[0])
        it+=1

def Execute(IC):
    define_functions(IC)
    call_func("main", [])
    run()
