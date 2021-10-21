#executes code.  #another thing it does is build the internal symbol dictionary from func name to definition, which can be done without executing the code.

from collections import defaultdict
from sys import exit
from functools import reduce
from ArityChecker import get_data_arities
from Stdlib import get_stdlib, stdlib_args, set_stdlib_funcs

#global_scope contains a function name mapped to a list of Function objects.
global_scope = defaultdict(lambda: [])
data_arities = {} #all data constructors act the same so a function definition is unecersarry. What is necersarry is an arity recording

#not 100% oo but it aids readability
class Function:
    def __init__(self, arguments, definition, primitive): #add type signature
        self.arguments = arguments
        self.definition = definition
        self.primitive = primitive #boolean to tell if function is primitive or not
    def __str__(self):
        return "function: " + ", ".join(map(str, self.arguments)) + " : " + str(self.definition) + " is " + str(self.primitive)

#not 100% oo but it aids readability
class Data:
    def __init__(self, name, data):
        self.name = name
        self.data = data
    def __str__(self):
        return self.name + "[" + ", ".join(map(str, self.data)) + "]"

#constructs args for a function object
    #as args are an ic constructing the arguments, rather than the actual arguments.
    #e.g: push a, successor (not real ic) which needs to become
        # s["a"] (not real repr)
def construct_args(args_in):
    args = []
    for n in reversed(args_in[1:]):
        if type(n) is not tuple: 
            args.append(Data(n, []))
        elif n[0] != "data-constructor": 
            raise Exception("non data constructor in argument definition") #should be moved to semantics checker
        else: 
            args.append(Data(n[1], [args.pop() for _ in range(data_arities[n[1]])])) #change later to handle multi arg constructors for custom types
    return args

#IC == Intermediate Code
def define_functions(IC):
    for n in IC: 
        if n[0] == "define".upper(): 
            global_scope[n[1][0][1]].append(Function(construct_args(n[1]), n[2], n[1][0][0]))
        #tuple repr is a little ugly

#calculates the depth of unary arithmetic. Useful in outputting the results of a file.
    #yikes need to re-write this or delete it
def depth(data: Data): #type data from execute.py
    if data.name == "!": return -1
    elif len(data.data) == 0: return 0
    else: return max(map(lambda n: n+1, map(depth, data.data))) #data.data is ugly naming, change later

#called in stdlib
def id_print(s):
    tmp = s.data_stack.pop()
    print(str(tmp), ":", depth(tmp))
    s.data_stack.append(tmp)

#note: although this is defined in stdlib, this should be used only by internal executor code to destroy stacks
def destroy(s, func_call):
    destroy_stack(func_call[1][2]) #ewwww

def destroy_self(s):
    for n in range(len(stacks)): #stacks defined later
        if s == stacks[n]: #equality defined through pointer equality i think so this should be fast enough?
            destroy_stack(n)
            break

def bottom(s):
    s.data_stack.append(Data("!", []))

set_stdlib_funcs(id_print, destroy, destroy_self, bottom) #the reason this exists is explained in Stdlib.py
stdlib = get_stdlib() #after we have set stdlib_funcs we need to set the stdlib variable

def call_stdlib(func_name, stack, func_call):
    if func_name == "destroy": #ewww please stop gross code :(
        destroy(stack, func_call)
        return
    """
    if len(stack.data_stack) != 0:
        tmp = stack.data_stack.pop()
        stack.data_stack.append(tmp)
        if tmp.name == "!": 
            return #what is happening here?
    """
    stdlib[func_name](stack)

#unifies a functions argument definniiton with the passed arguments. i.e: f(s[a]) passed with f(s[s[0]]) a becomes s[0]
def unify(definition, args):
    if definition == [] and args == []: return []
    if len(definition) != len(args): return False
    out = []
    for n in definition: #could zip to ensure one loop but this is easier
        tmp = unify_single(n, args.pop())
        if tmp == False: return False
        out += tmp
    return out

def unify_single(definition, arg): #unifies a single variable
    if definition.name in data_arities and definition.name != arg.name: return False
    elif definition.name not in data_arities: return [(definition.name, arg)] #check for non syntactical definitions (idk what this means but Im pretty sure we check that in the semantics checker)
    elif definition.name == arg.name and len(definition.data) != len(arg.data): return False
    elif definition.name == arg.name: 
        mapped = list(map(lambda n: unify_single(n[0], n[1]), zip(definition.data, arg.data)))
        for n in mapped: 
            if n == False: return False #can't use any or if not n due to auto type casting
        return reduce(lambda n1,n2: n1+n2, mapped, [])
    raise Exception("how did i get here?")

#checks which case of the function definitions is matched and returns that function.
def match_function(func_name, arguments):
    definitions = global_scope[func_name]
    if len(definitions) == 1 and arg_count(func_name) == 0: #no arguments (maybe check argument length)
        return [], definitions[0]
    for n in definitions:
        tmp_args = [n for n in arguments] #copying to avoid side affects
        tmp = unify(n.arguments, tmp_args)
        if tmp != False: return tmp, n #correctly unified
    return False, False #yikes, but what are you gonna do i guess (this is checked later)

def arg_count(func_name):
    if func_name in global_scope:
        tmp = global_scope[func_name][0] #assuming all functions have same arity
        return len(tmp.arguments)
    elif func_name in data_arities:
        return data_arities[func_name]
    elif func_name in stdlib:
        return stdlib_args[func_name] #defined earlier in the file
    else:
        raise Exception("unknown fuction called " + str(func_name))

#doesn't reutnr, instead modifies stacks
def call_user_defined_func(func_name, stack):
    arguments = [] #arguments to pass
    for _ in range(arg_count(func_name)):
        arguments.append(stack.data_stack.pop())
    scope, function = match_function(func_name, arguments)
    if scope == False and len(list(filter(lambda n: n.name=="!", arguments))) != 0: #if bottom passed as an argument and not matched
        stack.data_stack.append(Data("!", [])) #coudl have pushed id function to stack but this works better
        return #control flow return, intentionally left blank
    if scope == False:
        print("failed to match function ".upper() + str(func_name) + " with arguments ".upper() + str(list(map(str, arguments)))) #string call superfluous
        exit()
    for n in function.definition:
        stack.call_stack.append((scope, n, function.primitive))

#scope is a list [(var_name, value), ...]
def var_in_scope(name, scope):
    for n in scope: 
        if n[0] == name: return True
    return False

#gets the variable value (only ever gets called after var_in_scope checked)
def handle_var(name, scope, stack):
    for n in scope: 
        if n[0] == name: stack.data_stack.append(n[1])

def call_data(func_name, s):
    data_vals = []
    for n in range(data_arities[func_name]): data_vals.append(s.data_stack.pop()) #Might be able to simplify?
    s.data_stack.append(Data(func_name, data_vals))

#handles calling either stdlib, user_defined func or variable
def call_func(func_name, scope, stack, func_call): #although this function is simple, writing any more would be a violation of single function single responsibility
    #check for func_name in scope
    if var_in_scope(func_name, scope): handle_var(func_name, scope, stack)
    elif func_name in data_arities: call_data(func_name, stack)
    elif func_name in stdlib: call_stdlib(func_name, stack, func_call)
    else: call_user_defined_func(func_name, stack)

#should and probably could move stack stuff to separate file
class Stack:
    def __init__(self, call_stack, data_stack):
        self.call_stack = call_stack
        self.data_stack = data_stack
    def destroy(self):
        destroy_posses = get_destroy_positions(self)
        return destroy_posses + reduce(lambda l1,l2: l1+l2, [stacks[n].destroy() for n in destroy_posses], []) #stacks form tree so this is safe
    def clone(self):
        return Stack([n for n in self.call_stack], [n for n in self.data_stack])

stacks = []

def update_destroy(stack, add_am, destroy_posses):
    s = stack.call_stack
    pop_positions = []
    for i in range(len(s)):
        if type(s[i][1]) is str: continue
        if s[i][1][1] == "destroy" and s[i][1][2] in destroy_posses:
            pop_positions.append(i)
        if s[i][1][1] == "destroy":
            s[i] = (s[i][0], (s[i][1][0], s[i][1][1], s[i][1][2]+add_am), s[i][2])
    for i in reversed(pop_positions):
        s.pop(i)

def get_destroy_positions(stack): #code re use :(
    s = stack.call_stack
    out = []
    for i in range(len(s)):
        if type(s[i][1]) is str: continue
        if s[i][1][1] == "destroy":
            out.append(s[i][1][2])
    return out

def new_stack(stack):
    for n in stacks: #ugh i have to use a for loop instead of map cause impurities
        update_destroy(n, 1, {})
    stacks.insert(0, stack.clone())

#have to modify stack indexes
def destroy_stack(pos):
    destroy_posses = set([pos] + stacks[pos].destroy())
    change_am = 0
    for n in reversed(range(0, len(stacks))):
        if n in destroy_posses:
            change_am = change_am - 1
            stacks.pop(n)
        else:
            update_destroy(stacks[n], change_am, destroy_posses)

def debug_stacks(stacks, it_am, stack_num):
    print("it am = " + str(it_am))
    print("stack operation num =", stack_num)
    for i in range(len(stacks)):
        print("for stack " + str(i))
        #print("destroy pos", str(stacks[i].destroy_pos))
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

    i = 0 #stack index
    while (stacks[i].call_stack != []):

        #this is an extra thing only so far used with if but may be extended to other things later
        tmp = stacks[i].call_stack.pop()
        if type(tmp[1]) is str: #yikes I need to fix this
            call_func(tmp[1], tmp[0], stacks[i], tmp)
        else:
            if tmp[2] == "primitive" and tmp[1][0] == "non-primitive":
                new_stack(stacks[i])
                ac = arg_count(tmp[1][1])
                [stacks[0].data_stack.pop() for n in range(ac)] #maybe need to pop call_stack
                stacks[0].call_stack.append(([], ("data-constructor", "!"), "primitive"))
                i+=1 #stack index
                stacks[i].call_stack.append(([], ("primitive", "destroy", 0), "primitive"))
            call_func(tmp[1][1], tmp[0], stacks[i], tmp)

        i+=1
        if i >= len(stacks): i = 0 #loop back to the start of the stack

        it+=1
        debug_stacks(stacks, it, i)

    #print("finished!") #unecersarry but very fun :)
    debug_stacks(stacks, it+1)

def Execute(IC, execute=True): #IC = Intermediate code. execute == do we execute or just define functions
    global data_arities
    data_arities = get_data_arities()
    define_functions(IC)
    if execute:
        s = Stack([], []) #, False)
        stacks.append(s)
        call_func("main", [], s, None)
        run() #nothing passed, all are global variables :(
        if len(s.data_stack) == 0: return Data("!", [])
        return s.data_stack[0] #IMPORTANT: CHANGE LATER
    else:
        return None #little risky so make sure all calls to execute are properly checked

#used in the repl
def purge():
    global stacks
    stacks = []
    if "main" in global_scope:
        del global_scope["main"]
