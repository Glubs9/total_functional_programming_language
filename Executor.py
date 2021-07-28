from collections import defaultdict

global_scope = defaultdict(lambda: [])

def define_functions(IC):
    for n in IC: global_scope[n[1][-1][1]].append((n[1], n[2]))

stack = [] #i'm not too happy with stack being a global variable but I will change it later

stdlib = {}
def call_stdlib(func_name):
    #raise Exception("stdlib call not implemented yet")
    pass

def call_func(func_name):
    if func_name in stdlib: call_stdlib(func_name)

def Execute(IC):
    define_functions(IC)
    start_f = global_scope["main"]
