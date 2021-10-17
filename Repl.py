from Run import Run
from Executor import purge

#bit hardcoded but it kinda has to be
def Repl():
    purge()
    
    print("welcome to the repl")
    print("use an empty line to exit the repl")
    print()

    str_in = input(">>> ")
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
        str_in = input(">>> ")

    print()
    print("thanks for using the repl")
