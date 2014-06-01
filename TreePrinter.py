
import AST


def addToClass(cls):

    def decorator(func):
        setattr(cls,func.__name__,func)
        return func
    return decorator


class TreePrinter:
    
    @staticmethod
    def addAll(string,listToAdd):
        if type(listToAdd)==list:
            for item in listToAdd:
                if type(item) is list:
                    string=TreePrinter.addAll(string,item)
                else:
                    string=string+'\n'
                    for line in str(item).split('\n')[:-1]:
                        string = string + '| ' + line + '\n'
                    for line in str(item).split('\n')[-1:]:
                        string = string + '| ' + line
#                    print "&&"
#                    print string
#                    print "&&"
        return string
    
    @addToClass(AST.Node)
    def printTree(self):
        raise Exception("printTree not defined in class " + self.__class__.__name__)

    @addToClass(AST.Program)
    def printTree(self):
        return str(self.declarations)+'\n'+str(reduce(lambda x,y: str(x)+'\n'+str(y),self.fundefs))+'\n'+str(reduce(lambda x,y: str(x)+'\n'+str(y),self.instructions))

    @addToClass(AST.Decl)
    def printTree(self):
        if len(self.list)==0 : return ""
        toReturn="DECL"
        toReturn=TreePrinter.addAll(toReturn,self.list)
        return toReturn

    @addToClass(AST.Init)
    def printTree(self):
        toReturn = "="
        toReturn = TreePrinter.addAll(toReturn,[self.id])
        toReturn = TreePrinter.addAll(toReturn,[self.expression])
        return toReturn
    
    @addToClass(AST.ParExpr)
    def printTree(self):
        toReturn = str(self.expression)
        return toReturn
    
    @addToClass(AST.BinExpr)
    def printTree(self):
        toReturn = str(self.operator)
        toReturn = TreePrinter.addAll(toReturn,[self.first])
        toReturn = TreePrinter.addAll(toReturn,[self.second])
        return toReturn
    
    @addToClass(AST.FunExpr)
    def printTree(self):
        toReturn = self.id
        toReturn = TreePrinter.addAll(toReturn,self.expressionList)
        return toReturn
    
    @addToClass(AST.Arg)
    def printTree(self):
        toReturn="ARG " + str(self.id)
        return toReturn
    
    @addToClass(AST.FunDef)
    def printTree(self):
        toReturn="FUNDEF"
        toReturn=TreePrinter.addAll(toReturn,[self.id])
        toReturn=TreePrinter.addAll(toReturn,["RET " + str(self.type)])
        toReturn=TreePrinter.addAll(toReturn,self.argList)
        toReturn=TreePrinter.addAll(toReturn,[self.compoundInstr])
        return toReturn
        
    @addToClass(AST.CompoundInstr)
    def printTree(self):
        if len(str(self.declarations))>0 :
            return str(self.declarations)+'\n'+str(reduce(lambda x,y: str(x)+'\n'+str(y),self.instructions))
        else:
            return str(reduce(lambda x,y: str(x)+'\n'+str(y),self.instructions))
        
    @addToClass(AST.PrintInstr)
    def printTree(self):
        toReturn="PRINT"
        toReturn=TreePrinter.addAll(toReturn,[self.expression])
        return toReturn
    
    @addToClass(AST.LabeledInstr)
    def printTree(self):
        toReturn=":"
        toReturn=TreePrinter.addAll(toReturn,[self.id])
        toReturn=TreePrinter.addAll(toReturn,[self.instruction])
        return toReturn
    
    @addToClass(AST.Assignment)
    def printTree(self):
        toReturn="="
        toReturn=TreePrinter.addAll(toReturn,[self.id])
        toReturn=TreePrinter.addAll(toReturn,[self.expression])
        return toReturn

    @addToClass(AST.ChoiceInstr)
    def printTree(self):
        toReturn="IF"
        toReturn=TreePrinter.addAll(toReturn,[self.condition])
        toReturn=TreePrinter.addAll(toReturn,[self.instruction]) 
        if self.elseInstruction is not None :
            toReturn=toReturn+"\nELSE"
            toReturn=TreePrinter.addAll(toReturn,[self.elseInstruction]) 
        return toReturn
    
    @addToClass(AST.ReturnInstr)
    def printTree(self):     
        toReturn="RETURN"
        toReturn=TreePrinter.addAll(toReturn,[self.expression])
        return toReturn

    @addToClass(AST.WhileInstr)
    def printTree(self):   
        toReturn="WHILE"
        toReturn=TreePrinter.addAll(toReturn,[self.condition])
        toReturn=TreePrinter.addAll(toReturn,[self.instruction])
        return toReturn
    
    @addToClass(AST.RepeatInstr)
    def printTree(self): 
        toReturn="REPEAT"
        toReturn=TreePrinter.addAll(toReturn,[self.condition])
        toReturn=TreePrinter.addAll(toReturn,[self.instructions])
        return toReturn
        
        
        
    # @addToClass ...
    # ...
