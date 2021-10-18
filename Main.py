#this is the main file, it handles io and the integration of all the modules together.
#later on it would be worth separating these, i.e: io one file and integration another, but this
#project is small enough for now that it is not necersarry

from Run import Run
from Repl import Repl
from Executor import depth
import sys

stdlib_str = open("stdlib.tfpl", "r").read()
Run(stdlib_str, False) #do not execute main function

if not (len(sys.argv) == 2 or len(sys.argv) == 3):
    print("wrong number of arguments passed / Please pass a file")
    sys.exit()

if sys.argv[1] == "repl":
    Repl()
else:
    #could probably de-embed this
    inp_file = open(sys.argv[1]).read()
    if len(sys.argv) == 3:
        out = Run(inp_file, False)
        Repl()
    else:
        out = Run(inp_file)
        print("the output of running main{} in file " + sys.argv[1] + " is: ")
        print(out)
        print("with a depth of", depth(out))
