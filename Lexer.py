#lexes input into tokens
    #note: usually some form of union type with an enum is used for tokens, but python doesn't
    #handle these gracefully so I have opted to keep using strings.

TERMINALS = {"(", ")", "{", "}", "[", "]", ",", ";", "=", "0", "!", "|"}
WHITESPACE = {" ", "\t", "\n"}
def Lex(str_in): #continual string contatenation is not great timewise, change to arrays later.
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

def append_not_empty(li, string):
    if string != "":
        li.append(string)
