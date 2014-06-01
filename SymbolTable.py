#!/usr/bin/python


class FunSymbol(object):

    def __init__(self,type,id,argList):
        self.id=id
        self.type=type
        self.argList=argList

class SymbolTable(object):

    def __init__(self, parent, name):
        self.map={}
        self.parent=parent
        self.name=name

    def put(self, name, symbol):
        self.map[name]=symbol

    def get(self, name):
        if name in self.map :
            return self.map[name]
        return None
    
    def getIncludingParents(self, name):
        if name in self.map :
            return self.map[name]
        elif self.parent != None :
            return self.parent.getIncludingParents(name)
        return None

    def getParentScope(self):
        return self.parent

