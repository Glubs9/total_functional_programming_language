#maybe unecersarry class but it's better than more tuples
    #i had some great purity in my code up to this point

class CallStack:
    def __init__(self, stack):
        self.stack = stack #array of functions (of scope probably)?
        self.destroy_positions = [] #list of ints that when this stack encounters a destroy
                                    #function, will destroy all callstacks in this list
    def destroy_self(self, stacks):
        #clean up all reliant stacks in destroy positions
        #then destroy self
        pass
    def destroy_positions(self, stacks):
        #destroy all positions on this stack
        pass
    def move_positions_down(self, position):
        #if a stack gets destroyed, move all references down one
        pass
    def move_positions_up(self):
        #when a stack gets added to the stacks, it gets pushed to the front
        #after this is done all refrences have to be moved up
        pass
    def clone(self):
        copy = [n for n in self.stack] #please don't let function be modified (if function objects are not pure i am going to be sad)
        ret = CallStack(copy) #don't copy the destroy positions
        return

#considerations:
    #code is not pure :(
    #might have to delete references to an object when deleting it but this should be a tree anyway
        #so by definition (one path to each object) this shouldn't happen
