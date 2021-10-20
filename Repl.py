from Run import Run
from Executor import purge
from sys import exit
import signal

#bit hardcoded but it kinda has to be
def Repl():
    purge()
    
    print("welcome to the repl")
    print("ctrl+d, ctrl+c or a blank line will exit")
    print()

    str_in = get_input()
    while str_in != "":
        if ";" not in str_in:
            print("please use a semicolon at the end of the line") #i always forget lol
        elif "=" in str_in or "data" in str_in:
            print("error: definitions are not supported in the repl".upper())
        else:
            out = Run("main{} = " + str_in, True)
            print(out)
            purge()
        print()
        str_in = input(inp_str)

    print()
    print("thanks for using the repl")

inp_str = "--> "
def get_input():
    try:
        return input(inp_str)
    except EOFError:
        print()
        print("thanks for using the repl")
        exit()

#potentially change to be to just stop the current main process
    #definitely this would be good
def keyboard_interrupt(signal, frame):
    print("")
    print("")
    print("thank you for using the repl")
    exit()
signal.signal(signal.SIGINT, keyboard_interrupt)
