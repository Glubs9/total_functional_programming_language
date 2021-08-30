from collections import defaultdict
from sys import exit

global_scope = defaultdict(lambda: [])

class Function:
    def __init__(self, arguments, definition, primitive): #add type signature
        self.arguments = arguments
        self.definition = definition
        self.primitive = primitive #boolean to tell if function is primitive or not
    def __str__(self):
        return "function: " + " ,".join(map(str, self.arguments)) + " : " + str(self.definition) + " is " + str(self.primitive)

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
        global_scope[n[1][0][1]].append(Function(construct_args(n[1]), n[2], n[1][0][0])) #this is why we have to change from using tuples to objects (or tagged unions but they don't exist in python yet)

def id_print(s):
    tmp = s.data_stack.pop()
    print("print called with " + str(tmp))
    s.data_stack.append(tmp)

def destroy(s):
    destroy_stack(s.destroy_pos)

stdlib = {
        "id": lambda s: None, #id doesn't affect the stack so nothing happens (maybe change later)
        "0": lambda s: s.data_stack.append(Data('0', [])), 
        "s": lambda s: s.data_stack.append(Data('s', [s.data_stack.pop()])),
        "!": lambda s: s.data_stack.append(Data('!', [])),
        "destroy": destroy,
        "print": id_print
}
stdlib_args = {
        "id": 1, #kinda? not in the implementation but in the theory or something
        "0": 0,
        "s": 1,
        "!": 0,
        "destroy": 0,
        "print": 1
}

def call_stdlib(func_name, stack):
    if len(stack.data_stack) != 0:
        tmp = stack.data_stack.pop()
        stack.data_stack.append(tmp)
        if tmp.name == "!": return
    stdlib[func_name](stack)

def unify(definition, args):
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
    #hardcoded :(
def unify_single(definition, arg):
    if definition.name == "s" and arg.name == "s": return unify_single(definition.data[0], arg.data[0])
    elif definition.name == "s" and arg.name != "s": return False
    elif definition.name == "0" and arg.name == "0": return []
    elif definition.name == "0" and arg.name != "0": return False
    elif definition.name == "!" and arg.name == "!": return [] #have to specify that you unify with bottom
    elif definition.name == "!" and arg.name != "!": return False
    elif definition.name != "s": return (definition.name, arg) #check for non-snytacitcal definition
    else: raise Exception("how did i get here?")

#have to match the correct case and return the right function
def match_function(func_name, arguments):
    #check for empty function call
    #iterate through function definitions until correct case found
    definitions = global_scope[func_name]
    if len(definitions) == 1 and arg_count(func_name) == 0: #no arguments (maybe check argument length)
        return [], definitions[0]
    for n in definitions:
        tmp_args = [n for n in arguments] #copying to avoid side affects
        tmp = unify(n.arguments, tmp_args)
        if tmp != False: return tmp, n
    return False, False #yikes, but what are you gonna do i guess

def arg_count(func_name):
    if func_name in global_scope:
        tmp = global_scope[func_name][0] #assuming all functions have same arity
        return len(tmp.arguments)
    elif func_name in stdlib:
        return stdlib_args[func_name]
    else:
        raise Exception("unknown fuction called " + str(func_name))

def call_user_defined_func(func_name, stack):
    arguments = []
    for n in range(arg_count(func_name)):
        arguments.append(stack.data_stack.pop())
    scope, function = match_function(func_name, arguments) #can we do this?
    if scope == False and len(list(filter(lambda n: n.name=="!", arguments))) != 0: #if bottom passed as an argument and not matched
        stack.data_stack.append(Data("!", [])) #i can't remember how to make a function so i just did this
        return
    if scope == False:
        print("failed to match function " + str(func_name) + " with arguments " + str(list(map(str, arguments)))) #string call superfluous
        exit()
    for n in function.definition:
        stack.call_stack.append((scope, n, function.primitive))

#could with replac with any call
def var_in_scope(name, scope):
    for n in scope: 
        if n[0] == name: return True
    return False

def handle_var(name, scope, stack):
    for n in scope: 
        if n[0] == name: stack.data_stack.append(n[1])

def call_func(func_name, scope, stack): #although this function is simple, writing any more would be a violation of single function single responsibility
    #check for func_name in scope
    if var_in_scope(func_name, scope): handle_var(func_name, scope, stack)
    elif func_name in stdlib: call_stdlib(func_name, stack)
    else: call_user_defined_func(func_name, stack)

#should and probably could move stack stuff to separate file
class Stack:
    def __init__(self, call_stack, data_stack, destroy_pos=None):
        self.call_stack = call_stack
        self.data_stack = data_stack
        self.destroy_pos = destroy_pos
    def destroy(self):
        if self.destroy_pos == None: return []
        else: return [self.destroy_pos] + stacks[self.destroy_pos].destroy()
    def clone(self):
        return Stack([n for n in self.call_stack], [n for n in self.data_stack])

stacks = []

def new_stack(stack):
    for n in stacks: #ugh i have to use a for loop instead of map cause impurities
        n.destroy_pos+=1
    stacks.insert(0, stack.clone())

def destroy_stack(pos):
    destroy_posses = set([pos] + stacks[pos].destroy())
    change_am = 0
    for n in reversed(range(0, len(stacks))):
        if n in destroy_posses:
            change_am+=1
            stacks.pop(n)
        else:
            stacks[n].destroy_pos-=change_am

def debug_stacks(stacks, it_am):
    print("it am = " + str(it_am))
    for i in range(len(stacks)):
        print("for stack " + str(i))
        print("call_satck")
        for n in stacks[i].call_stack:
            print(n)
        print("data_stack")
        for n in stacks[i].data_stack:
            print(n)
        print("")
    print("")

def run():
    it = 1 #for debugging

    i = 0
    while (stacks[i].call_stack != []):
        #write better debug function for multiple stacks
        tmp = stacks[i].call_stack.pop()
        if type(tmp[1]) is str: #yikes I need to fix this
            #NEED TO ADD PRIMITIVE \ NONPRIMITVE CHECKING \ WE NEED TO FIX THIS \ DO THIS NEXT
            call_func(tmp[1], tmp[0], stacks[i])
        else:
            if tmp[2] == "primitive" and tmp[1][0] == "non-primitive":
                new_stack(stacks[i])
                #handle removing args from old stack, for this function
                ac = arg_count(tmp[1][1])
                [stacks[0].data_stack.pop() for n in range(ac)] #maybe need to pop call_stack
                stacks[0].call_stack.append(([], ("primitive", "!"), "primitive"))
                i+=1
                stacks[i].destroy_pos = 0 #should never cause out of bounds error cause stacks added to start of list
                stacks[i].call_stack.append(([], ("primitive", "destroy"), "primitive"))
            call_func(tmp[1][1], tmp[0], stacks[i])

        i+=1
        if i >= len(stacks): i = 0

        it+=1
        debug_stacks(stacks, it)

    print("finished!")
    #debug_stacks(stacks, it+1)

def Execute(IC, execute=True):
    define_functions(IC)
    if execute:
        s = Stack([], [], False)
        stacks.append(s)
        call_func("main", [], s)
        run()
        return s.data_stack[0] #IMPORTANT: CHANGE LATER
    else:
        return None #little risky so make sure all calls to execute are properly checked
