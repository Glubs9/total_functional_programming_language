def append_not_empty(li, string):
    if string != "":
        li.append(string)

TERMINALS = {"(", ")", "{", "}", "[", "]", ",", ";", "=", "$", "0"} #would be const if it could
WHITESPACE = {" ", "\t", "\n"}
def Lex(str_in):
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
