#!/usr/bin/python

from SymbolTable import SymbolTable
from SymbolTable import FunSymbol
from SymbolTable import ClassSymbol
import sys
import AST

class TypeChecker(object):
    
    def __init__(self):
        self.errorsOcurred=False
        self.classTables={}
        operators = ['+','-','*','/','%','|','&','^','&&','||','<<','>>','==','!=','<','>','<=','>=','f']
        self.types = ['int','float','string']
        self.ttype = dict((key,dict((key,{}) for key in self.types)) for key in operators)
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
        exc_type, exc_obj, exc_tb = sys.exc_info()
        print(exc_type, exc_tb.tb_lineno)
        print("********************************")

    def visit_Program(self,node):
        try:
            # print "visiting Program"
            self.symbolTable=SymbolTable(None,'main')
            node.classdefs.accept(self)
            node.declarations.accept(self)
            node.fundefs.accept(self)
            node.instructions.accept(self)
        except:
            self.error("could not continue parsing, correct errors first",0)

    def visit_Declarations(self,node):
        # print "visiting Declarations"
        for element in node.list :
            element.accept(self)
    
    def visit_Declaration(self,node):
        # print "visiting Declaration"
        toReturn = []
        declType = node.typeOrId
        allInits = node.initsOrClassinits.accept(self)
        if(declType in self.types):
            for element in allInits:
                [typeOrId,id] = element
                if self.symbolTable.get(id.value) != None:
                    self.error("Symbol: "+id.value+", was previusly declared",id.line)
                try:
                    self.ttype['f'][declType][typeOrId]
                except:
                    self.error("cannot initialize symbol of type: "+declType+", with expression of type: "+typeOrId,id.value)
                self.symbolTable.put(id.value,typeOrId)
                toReturn.append(id.value)
        else:
            typeOrId=declType.accept(self)
            for id in allInits:
                if self.symbolTable.get(id.value) != None:
                    self.error("Symbol: "+id.value+", was previusly declared",id.line)
                self.symbolTable.put(id.value,typeOrId)

                tmp = typeOrId
                while tmp!=None:
                    classTable = self.classTables[tmp.id]
                    for element in classTable.map:
                        self.symbolTable.put(self.makeClassContentName(typeOrId.id,id.value,element), classTable.get(element))
                    tmp=tmp.parentClass
                toReturn.append(id.value)
        return toReturn

    def makeClassContentName(self, className, objectName, fieldName):
        return "__"+className+objectName+fieldName

    def visit_Inits(self,node):
        # print "visiting Inits"
        toReturn=[]
        for element in node.list:
            toReturn.append(element.accept(self))
        return toReturn
    
    def visit_Init(self,node):
        # print "visiting Init"
        return [node.expression.accept(self),node.id]

    def visit_Classinits(self,node):
        # print "visiting Classinits"
        toReturn=[]
        for element in node.list:
            toReturn.append(element.accept(self))
        return toReturn

    def visit_Classinit(self,node):
        # print "visiting Classinit"
        return node.id

    def visit_Instructions(self,node):
        # print "visiting Instructions"
        self.symbolTable = SymbolTable(self.symbolTable,'instructions')
        for element in node.list :
            element.accept(self)
        self.symbolTable = self.symbolTable.getParentScope()
            
    def visit_PrintInstr(self,node):
        # print "visiting PrintInstr"
        if node.expression.accept(self) not in ['string','int','float']:
            self.error("cannot print expression of that type",node.line)
        
    def visit_LabeledInstr(self,node):
        # print "visiting LabeledInstr"
        node.instruction.accept(self)
    
    def visit_Assignment(self,node):
        # print "visiting Assignment"
        try:
            idType = node.access.accept(self)
            exprType = node.expression.accept(self)
            self.ttype['f'][idType][exprType]
        except:
            self.error("cannot assign "+exprType+" to "+idType,node.id.line)
            
    
    def visit_ChoiceInstr(self,node):
        # print "visiting ChoiceInstr"
        node.condition.accept(self)
        node.instruction.accept(self)
        node.elseInstruction.accept(self)
        
    def visit_Break(self,node):
        # print "visiting Break"
        pass
    
    def visit_Continue(self,node):
        # print "visiting Continue"
        pass
    
    def visit_WhileInstr(self,node):
        # print "visiting While"
        node.condition.accept(self)
        self.symbolTable = SymbolTable(self.symbolTable,'while')
        node.instruction.accept(self)
        self.symbolTable = self.symbolTable.getParentScope()
    
    def visit_RepeatInstr(self,node):
        # print "visiting Repeat"
        node.instructions.accept(self)
        node.condition.accept(self)
    
    def visit_ReturnInstr(self,node):
        # print "visiting Return"
        node.expression.accept(self) #todo check somehow
    
    def visit_CompoundInstr(self,node):
        # print "visiting CompoundInstr"
        #self.symbolTable = SymbolTable(self.symbolTable,'compoundInstr')
        node.declarations.accept(self)
        node.instructions.accept(self)
        #self.symbolTable = self.symbolTable.getParentScope()
    
    def visit_Condition(self,node):
        # print "visiting Condition"
        if node.expression.accept(self) not in ('int'):
            self.error("condition must be of int type",node.line)
    
    def visit_Integer(self,node):
        # print "visiting Integer"
        return 'int'
    
    def visit_Float(self,node):
        # print "visiting Float"
        return 'float'
    
    def visit_String(self,node):
        # print "visiting String"
        return 'string'
    
    def visit_Id(self,node):
        # print "visiting Id"
        if self.symbolTable.getIncludingParents(node.value):
            return self.symbolTable.getIncludingParents(node.value)
        self.error("undefined symbol: "+node.value,node.line)
    
    def visit_ParExpr(self,node):
        # print "visiting ParExpr"
        return node.expression.accept(self)   
        
    def visit_BinExpr(self,node):
        operator = node.operator
        first = node.first.accept(self)
        second = node.second.accept(self)            
            
        # print "visiting BinExpr"
        #print first
        #print operator
        #print second
        try:
            return self.ttype[operator][first][second]
        except:
            self.error("cannot compute operation: " +operator+",on arguments: "+first+", "+second,node.first.line)
            
          
    def visit_FunExpr(self,node):
        # print "visiting FunExpr"
        funSymbol = node.access.accept(self)
        for i in range(len(node.expressionList.list)):
            try:
                baseArgType = funSymbol.argList[i]
                givenArgType = node.expressionList.list[i].accept(self)
                self.ttype['f'][baseArgType][givenArgType]
            except:
                self.error("bad argument in funcall",node.line)
        return funSymbol.type
    
    def visit_ExprList(self,node):
        # print "visiting ExprList"
        toReturn = []
        for element in node.list:
            toReturn.append(element.accept(self))
        return toReturn
    
    def visit_FunDefs(self,node):
        # print "visiting FunDefs"
        for element in node.list :
            element.accept(self)
            
    def visit_FunDef(self,node):
        # print "visiting FunDef"
        self.symbolTable = SymbolTable(self.symbolTable,node.id.value)
        self.symbolTable.getParentScope().put(node.id.value,FunSymbol(node.typeOrId, node.id.value, map(lambda x: x.accept(self),node.argList.list)))
        node.compoundInstr.accept(self)
        self.symbolTable = self.symbolTable.getParentScope()
        return node.id.value
        
    def visit_ArgList(self,node):
        # print "visiting ArgList"
        toReturn = []
        for element in node.list:
            toReturn.append(element.accept(self))
        return toReturn
    
    def visit_Arg(self,node):
        # print "visiting Arg"
        self.symbolTable.put(node.id.value,node.typeOrId)
        return node.typeOrId

    def visit_ClassDefs(self,node):
        # print "visiting ClassDefs"
        for element in node.list :
            element.accept(self)

    def visit_ClassDef(self,node):
        # print "visiting ClassDef"
        self.symbolTable = SymbolTable(self.symbolTable if node.parentId == None else self.classTables[node.parentId.value], node.id.value)
        classSymbol = ClassSymbol(node.accessmodificator, node.id.value, node.parentId if node.parentId == None else node.parentId.accept(self),node.classcontent.accept(self))
        self.classTables[node.id.value]=self.symbolTable
        while self.symbolTable.parent!=None:
            self.symbolTable = self.symbolTable.getParentScope()
        self.symbolTable.put(node.id.value,classSymbol)



    def visit_Access(self,node):
        # print "visiting Access"
        accessedObject = node.list[0].accept(self)
        if(isinstance(accessedObject, ClassSymbol)):
            if(accessedObject.hasAccess(self.symbolTable.getFirstRelevantScopeName(),node.list[1].value)):
                classContentName = self.makeClassContentName(accessedObject.id,node.list[0].value,node.list[1].value)
                if self.symbolTable.getIncludingParents(classContentName):
                    accessedObject=self.symbolTable.getIncludingParents(classContentName)
                else:
                    self.error("cannot find class content "+classContentName,0)
            else:
                self.error("trying to access field that is not visible", 0)
        return accessedObject

    def visit_Fielddefs(self, node):
        # print "visiting Fielddefs"
        toReturn=[]
        for element in node.list:
            for accessAndId in element.accept(self):
                toReturn.append(accessAndId)
        return toReturn

    def visit_Fielddef(self, node):
        # print "visiting Fielddef"
        toReturn=[]
        for element in node.declaration.accept(self):
            toReturn.append((element,node.accessmodificator))
        return toReturn

    def visit_Classcontent(self, node):
        # print "visiting Classcontent"
        toReturn={}
        for element in node.fielddefs.accept(self):
            toReturn[element[0]]=element[1]
        for element in node.methoddefs.accept(self):
            toReturn[element[0]]=element[1]
        return toReturn

    def visit_Methoddefs(self, node):
        # print "visiting Methoddefs"
        toReturn=[]
        for element in node.list:
            toReturn.append(element.accept(self))
        return toReturn

    def visit_Methoddef(self, node):
        # print "visiting Methoddef"
        return (node.fundef.accept(self), node.accessmodificator)
    #def visit_Float(self, node):
    # ... 
    # 

    # ... 
    # 

