#!/usr/bin/python

from scanner import Scanner
import AST


class Cparser(object):
    def __init__(self):
        self.scanner = Scanner()
        self.scanner.build()
        self.errorsOccured = False

    tokens = Scanner.tokens

    precedence = (
        ("nonassoc", 'IFX'),
        ("nonassoc", 'ELSE'),
        ("right", '='),
        ("left", 'OR'),
        ("left", 'AND'),
        ("left", '|'),
        ("left", '^'),
        ("left", '&'),
        ("nonassoc", '<', '>', 'EQ', 'NEQ', 'LE', 'GE'),
        ("left", 'SHL', 'SHR'),
        ("left", '+', '-'),
        ("left", '*', '/', '%'),
    )


    def p_error(self, p):
        if p:
            print("Syntax error at line {0}, column {1}: LexToken({2}, '{3}')".format(p.lineno,
                                                                                      self.scanner.find_tok_column(p),
                                                                                      p.type, p.value))

        else:
            print('At end of input')
        self.errorsOccured = True

    def p_program(self, p):
        """program : classdefs declarations fundefs instructions"""
        p[0] = AST.Program(p[1], p[2], p[3], p[4])

    def p_declarations(self, p):
        """declarations : declarations declaration
                        | """
        if len(p) > 1:
            p[1].list.append(p[2])
            p[0] = p[1]
        else:
            p[0] = AST.Declarations()


    def p_declaration(self, p):
        """declaration : TYPE inits ';'
                       | id classinits ';'
                       | error ';' """
        if len(p) > 2:
            p[0] = AST.Declaration(p[1], p[2])
        else:
            p[0] = p[1]


    def p_inits(self, p):
        """inits : inits ',' init
                 | init """
        if len(p) > 2:
            p[1].list.append(p[3])
            p[0] = p[1]
        else:
            inits = AST.Inits()
            inits.list.append(p[1])
            p[0] = inits


    def p_init(self, p):
        """init : id '=' expression """
        p[0] = AST.Init(p[1], p[3])

    def p_classinits(self, p):
        """classinits : classinits ',' classinit
                      | classinit """
        if len(p) > 2:
            p[1].list.append(p[3])
            p[0] = p[1]
        else:
            classinits = AST.Classinits()
            classinits.list.append(p[1])
            p[0] = classinits

    def p_classinit(self, p):
        """classinit : id """
        p[0] = AST.Classinit(p[1])

    def p_instructions(self, p):
        """instructions : instructions instruction
                        | instruction """
        if len(p) == 2:
            instructions = AST.Instructions()
            instructions.list.append(p[1])
            p[0] = instructions
        else:
            p[1].list.append(p[2])
            p[0] = p[1]


    def p_instruction(self, p):
        """instruction : expression ';'
                       | print_instr
                       | labeled_instr
                       | assignment
                       | choice_instr
                       | while_instr 
                       | repeat_instr 
                       | return_instr
                       | break_instr
                       | continue_instr
                       | compound_instr"""
        p[0] = p[1]


    def p_print_instr(self, p):
        """print_instr : PRINT expression ';'
                       | PRINT error ';' """
        p[0] = AST.PrintInstr(p[2])


    def p_labeled_instr(self, p):
        """labeled_instr : id ':' instruction """
        p[0] = AST.LabeledInstr(p[1], p[3])

    def p_assignment(self, p):
        """assignment : access '=' expression ';' """
        p[0] = AST.Assignment(p[1], p[3])

    def p_access(self, p):
        """access : id
                  | id '.' id """

        if len(p) == 2:
            access = AST.Access(p.lineno(1))
            access.list.append(p[1])
            p[0] = access
        else:
            access = AST.Access(p.lineno(1))
            access.list.append(p[1])
            access.list.append(p[3])
            p[0] = access

    def p_choice_instr(self, p):
        """choice_instr : IF '(' condition ')' instruction  %prec IFX
                        | IF '(' condition ')' instruction ELSE instruction
                        | IF '(' error ')' instruction  %prec IFX
                        | IF '(' error ')' instruction ELSE instruction """
        if len(p) == 6:
            p[0] = AST.ChoiceInstr(p[3], p[5], None)
        else:
            p[0] = AST.ChoiceInstr(p[3], p[5], p[7])

    def p_while_instr(self, p):
        """while_instr : WHILE '(' condition ')' instruction
                       | WHILE '(' error ')' instruction """
        p[0] = AST.WhileInstr(p[3], p[5])


    def p_repeat_instr(self, p):
        """repeat_instr : REPEAT instructions UNTIL condition ';' """
        p[0] = AST.RepeatInstr(p[2], p[4])


    def p_return_instr(self, p):
        """return_instr : RETURN expression ';' """
        p[0] = AST.ReturnInstr(p[2])

    def p_continue_instr(self, p):
        """continue_instr : CONTINUE ';' """
        p[0] = AST.Continue()

    def p_break_instr(self, p):
        """break_instr : BREAK ';' """
        p[0] = AST.Break()


    def p_compound_instr(self, p):
        """compound_instr : '{' declarations instructions '}'"""
        p[0] = AST.CompoundInstr(p[2], p[3])


    def p_condition(self, p):
        """condition : expression"""
        p[0] = AST.Condition(p[1])

    def p_const(self, p):
        """const : integer
                 | float
                 | string"""
        p[0] = p[1]

    def p_integer(self, p):
        """integer : INTEGER"""
        p[0] = AST.Integer(p[1], p.lineno(1))

    def p_float(self, p):
        """float : FLOAT"""
        p[0] = AST.Float(p[1], p.lineno(1))

    def p_string(self, p):
        """string : STRING"""
        p[0] = AST.String(p[1][1:-1], p.lineno(1))

    def p_id(self, p):
        """id : ID"""
        p[0] = AST.Id(p[1], p.lineno(1))

    def p_expression(self, p):
        """expression : const
                      | access
                      | expression '+' expression
                      | expression '-' expression
                      | expression '*' expression
                      | expression '/' expression
                      | expression '%' expression
                      | expression '|' expression
                      | expression '&' expression
                      | expression '^' expression
                      | expression AND expression
                      | expression OR expression
                      | expression SHL expression
                      | expression SHR expression
                      | expression EQ expression
                      | expression NEQ expression
                      | expression '>' expression
                      | expression '<' expression
                      | expression LE expression
                      | expression GE expression
                      | '(' expression ')'
                      | '(' error ')'
                      | access '(' expr_list_or_empty ')'
                      | access '(' error ')' """
        if len(p) == 2:
            p[0] = p[1]
        elif p[1] == '(':
            p[0] = AST.ParExpr(p[2])
        elif len(p) == 4:
            p[0] = AST.BinExpr(p[1], p[2], p[3])
        else:
            p[0] = AST.FunExpr(p[1], p[3])


    def p_expr_list_or_empty(self, p):
        """expr_list_or_empty : expr_list
                              | """
        if len(p) == 1:
            p[0] = AST.ExprList()
        else:
            p[0] = p[1]

    def p_expr_list(self, p):
        """expr_list : expr_list ',' expression
                     | expression """
        if len(p) == 4:
            p[1].list.append(p[3])
            p[0] = p[1]
        else:
            toReturn = AST.ExprList()
            toReturn.list.append(p[1])
            p[0] = toReturn


    def p_fundefs(self, p):
        """fundefs : fundef fundefs
                   |  """
        if len(p) == 3:
            p[2].list.reverse()
            p[2].list.append(p[1])
            p[2].list.reverse()
            p[0] = p[2]
        else:
            p[0] = AST.FunDefs()

    def p_fundef(self, p):
        """fundef : TYPE id '(' args_list_or_empty ')' compound_instr
                  | id id '(' args_list_or_empty ')' compound_instr"""
        p[0] = AST.FunDef(p[1], p[2], p[4], p[6])

    def p_args_list_or_empty(self, p):
        """args_list_or_empty : args_list
                              | """
        if len(p) == 1:
            p[0] = AST.ArgList()
        else:
            p[0] = p[1]

    def p_args_list(self, p):
        """args_list : args_list ',' arg 
                     | arg """
        if len(p) == 2:
            argList = AST.ArgList()
            argList.list.append(p[1])
            p[0] = argList
        else:
            p[1].list.append(p[3])
            p[0] = p[1]

    def p_arg(self, p):
        """arg : TYPE id
               | id id"""
        p[0] = AST.Arg(p[1], p[2])

    def p_classdefs(self, p):
        """classdefs : classdef classdefs
                   |  """
        if len(p) == 3:
            p[2].list.reverse()
            p[2].list.append(p[1])
            p[2].list.reverse()
            p[0] = p[2]
        else:
            p[0] = AST.ClassDefs()

    def p_classdef(self, p):
        """classdef : accessmodificator CLASS id classcontent
                  | accessmodificator CLASS id EXTENDS id classcontent"""
        if len(p) < 7:
            p[0] = AST.ClassDef(p[1], p[3], None, p[4])
        else:
            p[0] = AST.ClassDef(p[1], p[3], p[5], p[6])

    def p_classcontent(self, p):
        """classcontent : '{' fielddefs ';' methoddefs '}' """
        p[0] = AST.Classcontent(p[2], p[4])

    def p_fielddefs(self, p):
        """fielddefs : fielddef fielddefs
                     | """
        if len(p) == 3:
            p[2].list.reverse()
            p[2].list.append(p[1])
            p[2].list.reverse()
            p[0] = p[2]
        else:
            p[0] = AST.Fielddefs()

    def p_fielddef(self, p):
        """fielddef : accessmodificator declaration """
        p[0] = AST.Fielddef(p[1], p[2])

    def p_methoddefs(self, p):
        """methoddefs : methoddef methoddefs
                     | """
        if len(p) == 3:
            p[2].list.reverse()
            p[2].list.append(p[1])
            p[2].list.reverse()
            p[0] = p[2]
        else:
            p[0] = AST.Methoddefs()

    def p_methoddef(self, p):
        """methoddef : accessmodificator fundef"""
        p[0] = AST.Methoddef(p[1], p[2])

    def p_accessmodificator(self,p):
        """accessmodificator : PRIVATE
                             | PROTECTED
                             | PUBLIC"""
        p[0] = p[1]
