from collections import defaultdict

global_scope = defaultdict(lambda: [])

class Function:
    def __init__(self, arguments, definition): #add type signature
        self.arguments = arguments
        self.definition = definition
    def __str__(self):
        return "function: " + " ,".join(map(str, self.arguments)) + " : " + str(self.definition)

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
        global_scope[n[1][0][1]].append(Function(construct_args(n[1]), n[2]))

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
    print("unification with the following" + " ,".join(map(str, definition)) + " with scope " + " ,".join(map(str, args)))
    if definition == [] and args == []: return []
    if len(definition) != len(args): return False
    out = []
    for n in definition: #could zip to ensure one loop
        tmp = unify_single(n, args.pop())
        if tmp == False: return False
        elif tmp == []: continue
        out.append(tmp)
    return out

#not pure
def unify_single(definition, arg):
    if definition.name == "s" and arg.name == "s": return unify_single(definition.data[0], arg.data[0])
    elif definition.name == "s" and arg.name != "s": return False
    elif definition.name == "0" and arg.name == "0": return []
    elif definition.name == "0" and arg.name != "0": return False
    elif definition.name != "s": return (definition.name, arg) #check for non-snytacitcal definition
    else: raise Exception("how did we get here?")

#have to match the correct case and return the right function
def match_function(func_name, arguments):
    #check for empty function call
    #iterate through function definitions until correct case found
    definitions = global_scope[func_name]
    if len(definitions) == 1 and arg_count(func_name) == 0: #no arguments (maybe check argument length)
        return [], definitions[0]
    for n in definitions:
        tmp_args = [n for n in arguments]
        tmp = unify(n.arguments, tmp_args)
        if tmp != False: return tmp, n
    print("no matching function found")
    raise Exception("branch not found yet")

def arg_count(func_name):
    print("getting argument count with func " + str(func_name))
    tmp = global_scope[func_name][0] #assuming all functions have same arity
    print("function is " + str(tmp))
    return len(tmp.arguments)

def call_user_defined_func(func_name):
    arguments = []
    for n in range(arg_count(func_name)):
        arguments.append(data_stack.pop())
    scope, function = match_function(func_name, arguments) #can we do this?
    print("in call user defined func" + str(function.definition))
    for n in function.definition:
        print("pushing to call_stack " + str((scope, n)))
        call_stack.append((scope, n))

#could with replac with any call
def var_in_scope(name, scope):
    print("testing var with scope + " + str(scope))
    for n in scope: 
        if n[0] == name: return True
    return False

def handle_var(name, scope):
    for n in scope: 
        if n[0] == name: data_stack.append(n[1])

def call_func(func_name, scope): #although this function is simple, writing any more would be a violation of single function single responsibility
    print()
    print("calling function " + func_name + " with scope " + " ,".join(map(str, scope)))
    print()
    #check for func_name in scope
    if var_in_scope(func_name, scope): handle_var(func_name, scope)
    elif func_name in stdlib: call_stdlib(func_name)
    else: call_user_defined_func(func_name)

#should and probably could move stack stuff to separate file
    #also follow the advice that if a class is a constructor and a method than it doesn't need to be a class
    #i feel it doesn't apply cause this is readability
#TODO:
    #integrate stacks array back into the rest of the code
    #then handle the creation and destruction of stacks
class Stack:
    def __init__(self, call_stack, data_stack, destroy_pos=None):
        self.call_stack = call_stack
        self.data_stack = data_stack
        self.destroy_pos = destroy_pos
    def destroy(self):
        if self.destroy_pos == None: return []
        else: return [self.destroy_pos] + stacks[self.destroy_pos].destroy()

stacks = []

def new_stack(stack):
    for n in stacks: #ugh i have to use a for loop instead of map cause impurities
        n.destroy_pos+=1
    stacks.insert(0, stack)

def destroy_stack(pos):
    destroy_posses = set([pos] + stacks[pos].destroy())
    change_am = 0
    for n in range(0, len(stacks), -1):
        if n in destroy_posses:
            change_am+=1
            stacks.pop(n)
        else:
            stacks[n].destroy_pos-=change_am

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
        it+=1

        tmp = call_stack.pop()
        print("tmp is = " + str(tmp))
        if type(tmp[1]) is str: #yikes I need to fix this
            call_func(tmp[1], tmp[0])
        else:
            call_func(tmp[1][1], tmp[0])

    print("finished!")
    print("call_stack")
    for n in call_stack:
        print(n)
    print("data_stack")
    for n in data_stack:
        print(n)
    print("")

def Execute(IC):
    define_functions(IC)
    call_func("main", [])
    run()
    return data_stack[0]
