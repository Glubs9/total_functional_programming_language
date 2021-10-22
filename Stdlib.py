#this file is used in the semantics checkers and executor so we put it here to avoid cyclic references (executor references aritychecker)
#although we could put it in the semantics checkers and have executor reference that, it would be poor form
#as the executor specific stuff is unecersarry for arityechecker to have. this is just better overall

id_print = None
destroy = None
destroy_self = None
bottom = None
split = None
def set_stdlib_funcs(id_print_in, destroy_in, destroy_self_in, bottom_in, split_in): #building it like this allows to not have to move all that logic here
    global id_print
    global destroy
    global destroy_self
    global bottom
    global split
    id_print = id_print_in
    destroy = destroy_in
    destroy_self = destroy_self_in
    bottom = bottom_in
    split = split_in

#used in executor. This is a function so that the used stdlib is the one that is updated after the
#set function sets the functions
def get_stdlib():
    stdlib = {
            "!": bottom,
            "print": id_print,
            "destroy": destroy, #what is destroy?
            "destroy_self": destroy_self,
            "split": split
    }
    return stdlib

#used in aritychecker and executor
stdlib_args = { 
        "!": 0,
        "destroy": 0,
        "destroy_self": 0, #maybe don't include here?
        "print": 1,
        "split": 0
}

#used in bracketchecker
stdlib_types = {
        "!": "data-constructor",
        "destroy": "non-primitive",
        "destroy_self": "non-primitive",
        "print": "primitive",
        "split": "non-primitive"
}
