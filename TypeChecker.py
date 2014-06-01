#!/usr/bin/python

from SymbolTable import SymbolTable
from SymbolTable import FunSymbol
import AST

class TypeChecker(object):
    
    def __init__(self):
        self.errorsOcurred=False
        operators = ['+','-','*','/','%','|','&','^','&&','||','<<','>>','==','!=','<','>','<=','>=','f']
        types = ['int','float','string']
        self.ttype = dict((key,dict((key,{}) for key in types)) for key in operators)
        self.ttype['+']['int']['float'] = 'float'
        self.ttype['+']['float']['int'] = 'float'
        self.ttype['+']['float']['float'] = 'float'
        self.ttype['+']['int']['int'] = 'int'
        self.ttype['+']['string']['string'] = 'string'

        self.ttype['-']['int']['float'] = 'float'
        self.ttype['-']['float']['int'] = 'float'
        self.ttype['-']['float']['float'] = 'float'
        self.ttype['-']['int']['int'] = 'int'

        self.ttype['*']['int']['float'] = 'float'
        self.ttype['*']['float']['int'] = 'float'
        self.ttype['*']['float']['float'] = 'float'
        self.ttype['*']['int']['int'] = 'int'
        
        self.ttype['/']['int']['float'] = 'float'
        self.ttype['/']['float']['int'] = 'float'
        self.ttype['/']['float']['float'] = 'float'
        self.ttype['/']['int']['int'] = 'int'

        self.ttype['%']['int']['int'] = 'int'

        self.ttype['|']['int']['int'] = 'int'

        self.ttype['&']['int']['int'] = 'int'

        self.ttype['^']['int']['int'] = 'int'

        self.ttype['&&']['int']['int'] = 'int'

        self.ttype['||']['int']['int'] = 'int'

        self.ttype['<<']['int']['int'] = 'int'

        self.ttype['>>']['int']['int'] = 'int'

        self.ttype['==']['int']['int'] = 'int'
        self.ttype['==']['int']['float'] = 'int'
        self.ttype['==']['float']['int'] = 'int'
        self.ttype['==']['float']['float'] = 'int'
        self.ttype['==']['string']['string'] = 'int'

        self.ttype['!=']['int']['int'] = 'int'
        self.ttype['!=']['int']['float'] = 'int'
        self.ttype['!=']['float']['int'] = 'int'
        self.ttype['!=']['float']['float'] = 'int'
        self.ttype['!=']['string']['string'] = 'int'

        self.ttype['<']['int']['int'] = 'int'
        self.ttype['<']['int']['float'] = 'int'
        self.ttype['<']['float']['int'] = 'int'
        self.ttype['<']['float']['float'] = 'int'
        self.ttype['<']['string']['string'] = 'int'

        self.ttype['>']['int']['int'] = 'int'
        self.ttype['>']['int']['float'] = 'int'
        self.ttype['>']['float']['int'] = 'int'
        self.ttype['>']['float']['float'] = 'int'
        self.ttype['>']['string']['string'] = 'int'

        self.ttype['<=']['int']['int'] = 'int'
        self.ttype['<=']['int']['float'] = 'int'
        self.ttype['<=']['float']['int'] = 'int'
        self.ttype['<=']['float']['float'] = 'int'
        self.ttype['<=']['string']['string'] = 'int'

        self.ttype['>=']['int']['int'] = 'int'
        self.ttype['>=']['int']['float'] = 'int'
        self.ttype['>=']['float']['int'] = 'int'
        self.ttype['>=']['float']['float'] = 'int'
        self.ttype['>=']['string']['string'] = 'int'
        
        self.ttype['f']['string']['string'] = 'string'
        self.ttype['f']['int']['int'] = 'int'
        self.ttype['f']['float']['float'] = 'float'
        self.ttype['f']['float']['int'] = 'float'
    
    def error(self,text,line):
        self.errorsOcurred=True
        print("********************************")
        print("Error: " + text)
        print("Line " + str(line))
        print("********************************")

    def visit_Program(self,node):
        try:
            #print "visiting Program"
            self.symbolTable=SymbolTable(None,'main')
            node.declarations.accept(self)
            node.fundefs.accept(self)
            node.instructions.accept(self)
        except:
            self.error("could not continue parsing, correct errors first",0)

    def visit_Declarations(self,node):
        #print "visiting Declarations"
        for element in node.list :
            element.accept(self)
    
    def visit_Declaration(self,node):
        #print "visiting Declaration"
        declType = node.type
        allInits = node.inits.accept(self)
        for element in allInits:
            [type,id] = element
            if self.symbolTable.get(id.value) != None:
                self.error("Symbol: "+id.value+", was previusly declared",id.line)
            try:
                self.ttype['f'][declType][type]
            except:
                self.error("cannot initialize symbol of type: "+declType+", with expression of type: "+type,id.value)
            self.symbolTable.put(id.value,type)
    
    def visit_Inits(self,node):
        #print "visiting Inits"
        toReturn=[]
        for element in node.list:
            toReturn.append(element.accept(self))
        return toReturn
    
    def visit_Init(self,node):
        #print "visiting Init"
        return [node.expression.accept(self),node.id]
    
    def visit_Instructions(self,node):
        #print "visiting Instructions"
        self.symbolTable = SymbolTable(self.symbolTable,'instructions')
        for element in node.list :
            element.accept(self)
        self.symbolTable = self.symbolTable.getParentScope()
            
    def visit_PrintInstr(self,node):
        #print "visiting PrintInstr"
        if node.expression.accept(self) not in ['string','int','float']:
            self.error("cannot print expression of that type",node.line)
        
    def visit_LabeledInstr(self,node):
        #print "visiting LabeledInstr"
        node.instruction.accept(self)
    
    def visit_Assignment(self,node):
        #print "visiting Assignment"
        if self.symbolTable.getIncludingParents(node.id.value) == None:
            self.error("unknown symbol name: "+id.value,id.line)
        try:
            idType = node.id.accept(self)
            exprType = node.expression.accept(self)
            self.ttype['f'][idType][exprType]
        except:
            self.error("cannot assign "+exprType+" to "+idType,node.id.line)
            
    
    def visit_ChoiceInstr(self,node):
        #print "visiting ChoiceInstr"
        node.condition.accept(self)
        node.instruction.accept(self)
        node.elseInstruction.accept(self)
        
    def visit_Break(self,node):
        #print "visiting Break"
        pass
    
    def visit_Continue(self,node):
        #print "visiting Continue"
        pass
    
    def visit_WhileInstr(self,node):
        #print "visiting While"
        node.condition.accept(self)
        self.symbolTable = SymbolTable(self.symbolTable,'while')
        node.instruction.accept(self)
        self.symbolTable = self.symbolTable.getParentScope()
    
    def visit_RepeatInstr(self,node):
        #print "visiting Repeat"
        node.instructions.accept(self)
        node.condition.accept(self)
    
    def visit_ReturnInstr(self,node):
        #print "visiting Return"
        node.expression.accept(self) #todo check somehow
    
    def visit_CompoundInstr(self,node):
        #print "visiting CompoundInstr"
        #self.symbolTable = SymbolTable(self.symbolTable,'compoundInstr')
        node.declarations.accept(self)
        node.instructions.accept(self)
        #self.symbolTable = self.symbolTable.getParentScope()
    
    def visit_Condition(self,node):
        #print "visiting Condition"
        if node.expression.accept(self) not in ('int'):
            self.error("condition must be of int type",node.line)
    
    def visit_Integer(self,node):
        #print "visiting Integer"
        return 'int'
    
    def visit_Float(self,node):
        #print "visiting Float"
        return 'float'
    
    def visit_String(self,node):
        #print "visiting String"
        return 'string'
    
    def visit_Id(self,node):
        #print "visiting Id"
        if self.symbolTable.getIncludingParents(node.value):
            return self.symbolTable.getIncludingParents(node.value)
        self.error("undefined symbol: "+node.value,node.line)
    
    def visit_ParExpr(self,node):
        #print "visiting ParExpr"
        return node.expression.accept(self)   
        
    def visit_BinExpr(self,node):
        operator = node.operator
        first = node.first.accept(self)
        second = node.second.accept(self)            
            
        #print "visiting BinExpr"
        #print first
        #print operator
        #print second
        try:
            return self.ttype[operator][first][second]
        except:
            self.error("cannot compute operation: " +operator+",on arguments: "+first+", "+second,node.first.line)
            
          
    def visit_FunExpr(self,node):
        #print "visiting FunExpr"
        funSymbol = self.symbolTable.getIncludingParents(node.id.value)
        for i in range(len(node.expressionList.list)):
            try:
                baseArgType = funSymbol.argList[i]
                givenArgType = node.expressionList.list[i].accept(self)
                self.ttype['f'][baseArgType][givenArgType]
            except:
                self.error("bad argument in funcall",node.line)
        return funSymbol.type
    
    def visit_ExprList(self,node):
        #print "visiting ExprList"
        toReturn = []
        for element in node.list:
            toReturn.append(element.accept(self))
        return toReturn
    
    def visit_FunDefs(self,node):
        #print "visiting FunDefs"
        for element in node.list :
            element.accept(self)
            
    def visit_FunDef(self,node):
        #print "visiting FunDef"
        self.symbolTable = SymbolTable(self.symbolTable,node.id.value)
        self.symbolTable.getParentScope().put(node.id.value,FunSymbol(node.type,node.id.value,map(lambda x : x.accept(self),node.argList.list)))
        node.compoundInstr.accept(self)
        self.symbolTable = self.symbolTable.getParentScope()
        
    def visit_ArgList(self,node):
        #print "visiting ArgList"
        toReturn = []
        for element in node.list:
            toReturn.append(element.accept(self))
        return toReturn
    
    def visit_Arg(self,node):
        #print "visiting Arg"
        self.symbolTable.put(node.id.value,node.type)
        return node.type 

    #def visit_Float(self, node):
    # ... 
    # 

    # ... 
    # 

