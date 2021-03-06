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

    def printIt(self):
        print "ZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZ"
        for key in self.map.iterkeys():
            print str(key) + " " + str(self.map[key])
        print "2222222222222222222222222222222222222222222222222222222"

class MemoryStack:
                                                                             
    def __init__(self, memory=None): # initialize memory stack with memory <memory>
        self.stack=[];
        if memory:
            self.stack.append(memory)

    def get(self, name):             # get from memory stack current value of variable <name>
        #print "get   " + str(name)
        for i in range(len(self.stack)-1,-1,-1):
            if self.stack[i].has_key(name):
                #print "      " + str(self.stack[i].get(name))
                return self.stack[i].get(name)
        #print "      None"
        return None
        
    def insert(self, name, value): # inserts into memory stack variable <name> with value <value>
        #print "insert    " + str(name) + " " + str(value)
        self.stack[-1].put(name, value)

    def printIt(self):
        self.stack[-1].printIt()
        
    def set(self, name, value): # sets variable <name> to value <value>
        #print "set    " + str(name) + " " + str(value)
        for i in range(len(self.stack)-1,-1,-1):
            if self.stack[i].has_key(name):
                self.stack[i].put(name,value)
                return True
        return False

    def push(self, memory): # push memory <memory> onto the stack
        self.stack.append(memory)

    def pop(self):          # pops the top memory from the stack
        return self.stack.pop()

    def addClassDef(self, dec, currClass, extension):
        #print "ADD: " + str(dec) + " " + str(currClass) + " " + str(extension)

        newExts = {}
        if extension != None:
            for i in range(len(self.stack)-1,-1,-1):
                for key in self.stack[i].map.iterkeys():
                    if str(key).startswith(str(extension)):
                        #print str(key)
                        currDecSuff = str(key).split('.')[1]
                        currVal = self.stack[i].get(key)
                        newExts[str(dec) +"." + currDecSuff] = [i, currVal]
        for key in newExts.iterkeys():
            #print "111111111111111111"
            #print str(newExts[key][0])
            #print str(newExts[key][1])
            #print str(key)
            #print "111111111111111111"
            self.stack[newExts[key][0]].put(key, newExts[key][1])

        newClass = {}
        for i in range(len(self.stack)-1,-1,-1):
            for key in self.stack[i].map.iterkeys():
                if str(key).startswith(str(currClass)):
                    #print str(key)
                    currDecSuff = str(key).split('.')[1]
                    currVal = self.stack[i].get(key)
                    currDec = str(dec) +"." + currDecSuff
                    newClass[currDec] = [i ,currVal]

        for key in newClass.iterkeys():
            #print "2222222222222222222222222"
            #print str(newClass[key][0])
            #print str(newClass[key][1])
            #print str(key)
            #print "2222222222222222222222222"
            self.stack[newClass[key][0]].put(key, newClass[key][1])