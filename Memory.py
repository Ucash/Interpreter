class Function:
    def __init__(self,id,argList,compoundInstr):
        self.compoundInstr=compoundInstr
        self.id=id
        self.argList=argList

class Memory:

    def __init__(self, name): # memory name
        self.name=name
        self.map={}

    def has_key(self, name):  # variable name
        return (name in self.map)

    def get(self, name):         # get from memory current value of variable <name>
        return self.map[name]
    
    def put(self, name, value):  # puts into memory current value of variable <name>
        self.map[name]=value


class MemoryStack:
                                                                             
    def __init__(self, memory=None): # initialize memory stack with memory <memory>
        self.stack=[];
        if memory:
            self.stack.append(memory)

    def get(self, name):             # get from memory stack current value of variable <name>
        for i in range(len(self.stack)-1,-1,-1):
            if self.stack[i].has_key(name):
                return self.stack[i].get(name)
        return None
        
    def insert(self, name, value): # inserts into memory stack variable <name> with value <value>
        self.stack[-1].put(name, value)
        
    def set(self, name, value): # sets variable <name> to value <value>
        for i in range(len(self.stack)-1,-1,-1):
            if self.stack[i].has_key(name):
                self.stack[i].put(name,value)
                return True
        return False

    def push(self, memory): # push memory <memory> onto the stack
        self.stack.append(memory)

    def pop(self):          # pops the top memory from the stack
        return self.stack.pop()
