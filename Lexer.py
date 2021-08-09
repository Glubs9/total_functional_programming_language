from sys import exit

def append_not_empty(li, string):
    if string != "":
        li.append(string)

TERMINALS = {"(", ")", "{", "}", "[", "]", ",", ";", "=", "0"}
WHITESPACE = {" ", "\t", "\n"}
def Lex(str_in):
    #maybe shouldn't go here but I don't really see another place to put it
    if len([n for n in str_in if n == ";"]) != len([n for n in str_in if n == "="]):
        print("ERROR: NON MATCHING AMOUNT OF SEMI COLONS AND DEFINITIONS")
        exit()
    out = []
    tmp = ""
    for n in str_in:
        if n in TERMINALS:
            append_not_empty(out, tmp)
            tmp = ""
            out.append(n)
        elif n in WHITESPACE:
            append_not_empty(out, tmp)
            tmp = ""
        else:
            tmp += n
    append_not_empty(out, tmp)
    return out
