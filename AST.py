class Node(object):
    #def __str__(self):
    #    return self.printTree()
    def accept(self, visitor):
        return getattr(visitor, 'visit_' + self.__class__.__name__)(self)

    def acceptInt(self, visitor):
        return visitor.visit(self)

    def setLineNo(line):
        self.line = line


class Program(Node):
    def __init__(self, classdefs, declarations, fundefs, instructions):
        self.classdefs = classdefs
        self.declarations = declarations
        self.fundefs = fundefs
        self.instructions = instructions


class Declarations(Node):
    def __init__(self):
        self.list = []


class Declaration(Node):
    def __init__(self, typeOrId, initsOrClassinits):
        self.typeOrId = typeOrId
        self.initsOrClassinits = initsOrClassinits


class Inits(Node):
    def __init__(self):
        self.list = []


class Init(Node):
    def __init__(self, id, expression):
        self.id = id
        self.expression = expression


class Classinits(Node):
    def __init__(self):
        self.list = []


class Classinit(Node):
    def __init__(self, id):
        self.id = id


class Instructions(Node):
    def __init__(self):
        self.list = []


class ParExpr(Node):
    def __init__(self, expression):
        self.expression = expression
        self.line = expression.line


class BinExpr(Node):
    def __init__(self, first, operator, second):
        self.first = first
        self.operator = operator
        self.second = second
        self.line = first.line


class ExprList(Node):
    def __init__(self):
        self.list = []


class FunDefs(Node):
    def __init__(self):
        self.list = []


class FunExpr(Node):
    def __init__(self, access, expressionList):
        self.access = access
        self.expressionList = expressionList
        self.line = access.line


class FunDef(Node):
    def __init__(self, typeOrId, id, argList, compoundInstr):
        self.typeOrId = typeOrId
        self.id = id
        self.argList = argList
        self.compoundInstr = compoundInstr


class ArgList(Node):
    def __init__(self):
        self.list = []


class Arg(Node):
    def __init__(self, typeOrId, id):
        self.typeOrId = typeOrId
        self.id = id


class PrintInstr(Node):
    def __init__(self, expression):
        self.expression = expression


class LabeledInstr(Node):
    def __init__(self, id, instruction):
        self.id = id
        self.instruction = instruction


class Assignment(Node):
    def __init__(self, access, expression):
        self.access = access
        self.expression = expression


class Access(Node):
    def __init__(self, line):
        self.list = []
        self.line = line


class CompoundInstr(Node):
    def __init__(self, declarations, instructions):
        self.declarations = declarations
        self.instructions = instructions


class Condition(Node):
    def __init__(self, expression):
        self.expression = expression


class ChoiceInstr(Node):
    def __init__(self, condition, instruction, elseInstruction):
        self.condition = condition
        self.instruction = instruction
        self.elseInstruction = elseInstruction


class Break(Node):
    def __init__(self):
        pass


class Continue(Node):
    def __init__(self):
        pass


class WhileInstr(Node):
    def __init__(self, condition, instruction):
        self.condition = condition
        self.instruction = instruction


class RepeatInstr(Node):
    def __init__(self, instructions, condition):
        self.instructions = instructions
        self.condition = condition


class ReturnInstr(Node):
    def __init__(self, expression):
        self.expression = expression


class Integer(Node):
    def __init__(self, value, line):
        self.value = value
        self.line = line


class Float(Node):
    def __init__(self, value, line):
        self.value = value
        self.line = line


class String(Node):
    def __init__(self, value, line):
        self.value = value
        self.line = line


class Id(Node):
    def __init__(self, value, line):
        self.value = value
        self.line = line


class ClassDefs(Node):
    def __init__(self):
        self.list = []


class ClassDef(Node):
    def __init__(self, accessmodificator, id, parentId, classcontent):
        self.accessmodificator = accessmodificator
        self.id = id
        self.parentId = parentId
        self.classcontent = classcontent


class Classcontent(Node):
    def __init__(self, fielddefs, methoddefs):
        self.fielddefs = fielddefs
        self.methoddefs = methoddefs


class Fielddefs(Node):
    def __init__(self):
        self.list = []


class Fielddef(Node):
    def __init__(self, accessmodificator, declaration):
        self.accessmodificator = accessmodificator
        self.declaration = declaration


class Methoddefs(Node):
    def __init__(self):
        self.list = []


class Methoddef(Node):
    def __init__(self, accessmodificator, fundef):
        self.accessmodificator = accessmodificator
        self.fundef = fundef

        # ...