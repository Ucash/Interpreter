import AST
import SymbolTable
from Memory import *
from Exceptions import  *
from visit import *


class Interpreter(object):


    @on('node')
    def visit(self, node):
        pass

    @when(AST.Program)
    def visit(self,node):
        #print "visiting Program"
        self.mainMemory=MemoryStack(Memory('main'))
        self.functionMemory=MemoryStack()
        
        node.declarations.acceptInt(self)
        node.fundefs.acceptInt(self)
        node.instructions.acceptInt(self)

    @when(AST.Declarations)
    def visit(self,node):
        #print "visiting Declarations"
        for element in node.list :
            element.acceptInt(self)
    
    @when(AST.Declaration)
    def visit(self,node):
        #print "visiting Declaration"
        declType = node.type
        allInits = node.inits.acceptInt(self)
        for element in allInits:
            [id,value] = element
            self.mainMemory.insert(id,value)
    
    @when(AST.Inits)
    def visit(self,node):
        #print "visiting Inits"
        toReturn=[]
        for element in node.list:
            toReturn.append(element.acceptInt(self))
        return toReturn
    
    @when(AST.Init)
    def visit(self,node):
        #print "visiting Init"
        return [node.id.value,node.expression.acceptInt(self)]
    
    @when(AST.Instructions)
    def visit(self,node):
        #print "visiting Instructions"
        for element in node.list :
            element.acceptInt(self)
           
    @when(AST.PrintInstr)       
    def visit(self,node):
        #print "visiting PrintInstr"
        print(node.expression.acceptInt(self))

    @when(AST.LabeledInstr)    
    def visit(self,node):
        #print "visiting LabeledInstr"
        node.instruction.acceptInt(self)
    
    @when(AST.Assignment)  
    def visit(self,node):
        #print "visiting Assignment"
        id = node.id.value
        value = node.expression.acceptInt(self)
        if not self.functionMemory.set(id,value):
            self.mainMemory.set(id,value)
        return value
        
    @when(AST.ChoiceInstr) 
    def visit(self,node):
        #print "visiting ChoiceInstr"
        if node.condition.acceptInt(self):
            return node.instruction.acceptInt(self)
        else:
            return node.elseInstruction.acceptInt(self)
    
    @when(AST.Break)
    def visit(self,node):
        #print "visiting Break"
        raise BreakException()
    
    @when(AST.Continue)
    def visit(self,node):
        #print "visiting Continue"
        raise ContinueException
    
    @when(AST.WhileInstr)
    def visit(self,node):
        #print "visiting While"
        r = None
        try:
            while node.condition.acceptInt(self):
                try:
                    r = node.instruction.acceptInt(self)
                except ContinueException:
                    r = None
        except BreakException:
            r = None
        return r
    
    @when(AST.RepeatInstr)
    def visit(self,node):
        #print "visiting Repeat"
        r = None
        try:
            while True:
                try:
                    r = node.instructions.acceptInt(self)
                except ContinueException:
                    r=None
                    continue
                if node.condition.acceptInt(self):
                    break
        except BreakException:
            r = None
        return r
    
    @when(AST.ReturnInstr)
    def visit(self,node):
        #print "visiting Return"
        raise ReturnValueException(node.expression.acceptInt(self))
    
    @when(AST.CompoundInstr)
    def visit(self,node):
        #print "visiting CompoundInstr"
        self.mainMemory.push(Memory('compoundInstr'))
        self.functionMemory.push(Memory('compoundInstr'))
        try:
            node.declarations.acceptInt(self)
            node.instructions.acceptInt(self)
        except Exception as e:
            raise e
        finally:
            self.mainMemory.pop()
            self.functionMemory.pop()
  
    @when(AST.Condition)
    def visit(self,node):
        #print "visiting Condition"
        if node.expression.acceptInt(self) in [0,None]:
            return False
        return True
    
    @when(AST.Integer)
    def visit(self,node):
        #print "visiting Integer"
        return int(node.value)
    
    @when(AST.Float)
    def visit(self,node):
        #print "visiting Float"
        return float(node.value)
    
    @when(AST.String)
    def visit(self,node):
        #print "visiting String"
        return node.value
    
    @when(AST.Id)
    def visit(self,node):
        #print "visiting Id"
        if self.functionMemory.get(node.value) != None:
            return self.functionMemory.get(node.value)
        return self.mainMemory.get(node.value)
    
    @when(AST.ParExpr)
    def visit(self,node):
        #print "visiting ParExpr"
        return node.expression.acceptInt(self)   
    
    @when(AST.BinExpr)
    def visit(self,node):
        #print "visiting BinExpr"
        operator = node.operator
        first = node.first.acceptInt(self)
        second = node.second.acceptInt(self)               
        #print first
        #print operator
        #print second
        if operator=='+' : return first + second
        elif operator=='-' : return first - second
        elif operator=='*' : return first * second
        elif operator=='/' : return first / second
        elif operator=='%' : return first % second
        elif operator=='|' : return first | second
        elif operator=='&' : return first & second
        elif operator=='&&' : return first and second
        elif operator=='||' : return first or second
        elif operator=='<<' : return first << second
        elif operator=='>>' : return first >> second
        elif operator=='==' : return first == second
        elif operator=='!=' : return first != second
        elif operator=='<' : return first < second
        elif operator=='>' : return first > second
        elif operator=='<=' : return first <= second
        elif operator=='>=' : return first >= second
            
    @when(AST.FunExpr)      
    def visit(self,node):
        #print "visiting FunExpr"
        
        fun = self.mainMemory.get(node.id.value)
        givenArgValues = node.expressionList.acceptInt(self)
        self.functionMemory.push(Memory(node.id.value))
        for i in range(len(fun.argList)):
            self.functionMemory.insert(fun.argList[i],givenArgValues[i])
        try:
            fun.compoundInstr.acceptInt(self)
        except ReturnValueException as e:
            return e.value
        finally:
            self.functionMemory.pop()
     
    @when(AST.ExprList)  
    def visit(self,node):
        #print "visiting ExprList"
        toReturn = []
        for element in node.list:
            toReturn.append(element.acceptInt(self))
        return toReturn
    
    @when(AST.FunDefs) 
    def visit(self,node):
        #print "visiting FunDefs"
        for element in node.list :
            element.acceptInt(self)
    
    @when(AST.FunDef) 
    def visit(self,node):
        #print "visiting FunDef"
        fun = Function(node.id,node.argList.acceptInt(self),node.compoundInstr)
        self.mainMemory.insert(fun.id.value,fun)
    
    @when(AST.ArgList) 
    def visit(self,node):
        #print "visiting ArgList"
        toReturn = []
        for element in node.list:
            toReturn.append(element.acceptInt(self))
        return toReturn
    
    @when(AST.Arg) 
    def visit(self,node):
        #print "visiting Arg"
        return node.id.value 

    #def visit_Float(self, node):
    # ... 
    # 

    # ... 
    # 



