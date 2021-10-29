#runs the repl

from Run import Run
from Executor import purge
from sys import exit
import signal
import readline

try:
    readline.read_history_file()
except FileNotFoundError:
    readline.write_history_file()

#bit hardcoded but it kinda has to be
def Repl():
    purge()
    
    print("welcome to the repl")
    print("ctrl+d will exit")
    print()

    str_in = get_input()
    while True:
        if str_in == False:
            pass
        elif ";" not in str_in:
            print("please use a semicolon at the end of the line") #i always forget lol
        elif "=" in str_in or "data" in str_in:
            print("error: definitions are not supported in the repl".upper())
        else:
            try:
                out = Run("main{} = " + str_in, True)
                readline.append_history_file(1)
                print(out)
            except KeyboardInterrupt:
                print("")
                print("error: KeyboardInterrupt".upper())
            purge()
        str_in = get_input()

def get_input():
    try:
        try:
            return input("--> ")
        except KeyboardInterrupt:
            print()
            return False
    except EOFError:
        print("")
        print("")
        print("thank you for using the repl")
        exit()
