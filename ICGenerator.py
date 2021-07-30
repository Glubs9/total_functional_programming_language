#intermediate code generator
#trying to build a stack based representation of the input code, similar to a forth or something?
from functools import reduce

#note: I haven't thought about how to unify on stack based code but it would probably work?

#this is a little dense but a little clever isn't it
def func_call_gen(arr_in):
    if len(arr_in) <= 1: return arr_in
    return [(arr_in[0], arr_in[1])] + \
        reduce(lambda a,b: a+b, list(
                map(func_call_gen, arr_in[2])
        ))

#maybe change this later?
def stackify_line(line_in):
    return ("DEFINE", func_call_gen(line_in[1]), func_call_gen(line_in[2]))

def Generate_IC(lines_in):
    return list(map(stackify_line, lines_in))
