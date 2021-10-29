#this file preprocessess the string

from sys import exit

def PreProcess(str_in):
    str_in = remove_comments(str_in)
    if not check_brackets(str_in):
        print("error: unbalanced brackets or mismatched brackets".upper())
        exit()
    elif not check_balanced_semicolons(str_in):
        print("error: non-matching amount of semi-colons and definitions".upper())
        exit()
    return str_in

brackets = {"(" : ")", "{" : "}", "[" : "]"}
opening = {k for k,v in brackets.items()} #maybe a little unecersarry but renaming makes it more readable
closing = {v for k,v in brackets.items()} #maybe a little unecersarry but this makes it faster
def check_brackets(str_in): #checks balanced brackets
    stack = []
    for n in str_in:
        if   n in closing and len(stack) == 0: return False #formatting :)))))
        elif n in closing and brackets[stack.pop()] != n: return False
        elif n in opening: stack.append(n)
    if len(stack) != 0: return False
    return True

def check_balanced_semicolons(str_in): #check there is equal amount of semi colons and =
    return len([n for n in str_in if n == ";"]) == len([n for n in str_in if n == "="]) 

import re
def remove_comments(str_in): #regular expression causes error with embedded comments.
    return re.sub("/\*.*?\*/", "", str_in, flags=re.DOTALL)
