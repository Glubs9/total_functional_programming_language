#this file preprocessess the string
#as of yet it only checks for balanced brackets and balanced definitions
    #this functionality could be moved but it is easiest to write and understand if it is here.
#more may be added to this file later

from sys import exit

def PreProcess(str_in):
    str_in = remove_comments(str_in)
    if not check_brackets(str_in):
        print("error: unbalanced brackets or mismatched brackets".upper())
        exit()
    elif not check_balanced_semicolons(str_in):
        print("error: non-matching amount of semi-colons and definitions".upper())
    return str_in

brackets = {"(" : ")", "{" : "}", "[" : "]"}
opening = {k for k,v in brackets.items()} #maybe a little unecersarry but renaming makes it more readable
closing = {v for k,v in brackets.items()} #maybe a little unecersarry but this makes it faster
def check_brackets(str_in):
    stack = []
    for n in str_in:
        if   n in closing and len(stack) == 0: return False #formatting :)))))
        elif n in closing and brackets[stack.pop()] != n: return False
        elif n in opening: stack.append(n)
    if len(stack) != 0: return False
    return True

def check_balanced_semicolons(str_in):
    return len([n for n in str_in if n == ";"]) == len([n for n in str_in if n == "="]) 

import re
def remove_comments(str_in):
    return re.sub("/\*.*?\*/", "", str_in, flags=re.DOTALL)
