#intermediate code generator
    #builds a stack based representation of the code.
    #equivalent to a post-order traversal of the ast

from functools import reduce

#post order traversal
def func_call_gen(arr_in):
    if len(arr_in) <= 1: return arr_in
    return [(arr_in[0], arr_in[1])] + \
        reduce(lambda a,b: a+b, list(
                map(func_call_gen, arr_in[2])
        ))

def stackify_line(line_in):
    return ("DEFINE", func_call_gen(line_in[1]), func_call_gen(line_in[2]))

def Generate_IC(lines_in):
    return list(map(stackify_line, lines_in))
