#checks there is no literal with s[!]

from sys import exit

def Bottom_Checker(funcs):
    for n in funcs:
        if not all(map(check, n[1][2] + [n[2]])): #this is a little unreadable from the tuple ast repr. Potential to change it later
            print("error: function \"".upper() + n[1][1] + "\" uses a literal successor on a bottom type (e.g: s[!])".upper())
            exit()
    return True

#i do want to refactor the long if statement below but it is a side effect of the tuple reprsentation so not much can be done?
    #not much I can do to make this more readable.
def check(code):
    if type(code) is not list and type(code) is not tuple: return True
    elif type(code) is list and len(code) == 1: return True
    elif type(code) is tuple and code[0] == "data-constructor" and code[1] == "s" and type(code[2]) is list and len(code[2]) == 1 and len(code[2][0]) == 1 and code[2][0][0] == "!": return False
    elif type(code) is tuple: return all(map(check, code[2]))
    elif type(code) is list:
        return all(map(check, code))
    raise Exception("in bottom checker, got to unreachable case with code = " + str(code))
