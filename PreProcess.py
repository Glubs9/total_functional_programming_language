from sys import exit

def PreProcess(str_in):
    if not check_brackets(str_in):
        print("error: unbalanced brackets or mismatched brackets".upper())
        exit()
    return str_in

brackets = {"(" : ")", "{" : "}", "[" : "]"}
opening = {k for k,v in brackets.items()}
closing = {v for k,v in brackets.items()}
def check_brackets(str_in):
    stack = []
    for n in str_in:
        if   n in closing and len(stack) == 0: return False
        elif n in closing and brackets[stack.pop()] != n: return False
        elif n in opening: stack.append(n)
    if len(stack) != 0: return False
    return True
