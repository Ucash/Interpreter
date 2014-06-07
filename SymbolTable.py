# !/usr/bin/python


class FunSymbol(object):
    def __init__(self, type, id, argList):
        self.id = id
        self.type = type
        self.argList = argList


class ClassSymbol(object):
    def __init__(self, accessModificator, id, parentClass, content):
        self.id = id
        self.accessModificator = accessModificator
        self.parentClass = parentClass
        self.contentAccessModificators = content

    def hasAccess(self, scopeName, name):
        access = self.getAccess(name)
        searchedInParents=False
        if access == None:
            access=self.findParentAccess(name);
            searchedInParents=True
        if (access == "public"):
            return True
        elif (not searchedInParents and access == "private" and scopeName == self.id):
            return True
        elif (access == "protected" and scopeName == self.id):
            return True
        return False

    def findParentAccess(self, name):
        parent = self.parentClass
        while(parent != None):
            access = parent.getAccess(name)
            if(access!=None):
                return access
            parent=parent.parentClass
        return None

    def getAccess(self, name):
        if (name in self.contentAccessModificators):
            return self.contentAccessModificators[name]
        return None

class SymbolTable(object):
    def __init__(self, parent, name):
        self.map = {}
        self.parent = parent
        self.name = name

    def put(self, name, symbol):
        self.map[name] = symbol

    def get(self, name):
        if name in self.map:
            return self.map[name]
        return None

    def getIncludingParents(self, name):
        if name in self.map:
            return self.map[name]
        elif self.parent != None:
            return self.parent.getIncludingParents(name)
        return None

    def getParentScope(self):
        return self.parent

    def getFirstRelevantScopeName(self):
        irrelevantNames = ["instructions", "while"]
        if(self.name in irrelevantNames):
            return self.parent.getFirstRelevantScopeName()
        return self.name;