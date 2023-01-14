import ply.yacc as yacc
import sys
import kino_lex
import kino_compile
import kino_env
import copy


tokens = kino_lex.tokens


def p_error(t):
   print ( "Syntax error: Line %d: Unexpected '%s'" % (t.lexer.lineno, t.value) )
   #todo: Syntax error's should be fatal, but its helpful for debugging the tree for now
   #sys.exit(-1)

def p_program_entire ( t ):
   '''file : program'''
   t[0] = t[1]
   print(".text")
   kino_compile.compile ( t[0], kino_env.empty_environment ( ), 32 )
def p_program_expr(t):
   '''program : line
               | line program'''
   if len ( t ) == 2:
      t[0] = kino_compile.Tree_Node ( kino_compile.ntProgram, None, t[1], t.lexer.lineno )
   else:
      t[0] = kino_compile.Tree_Node ( kino_compile.ntProgram, [t[2]], t[1], t.lexer.lineno )

def p_line_expr(t):
   '''line : declaration
         | assignment
         | control
         | wait'''
   t[0] = kino_compile.Tree_Node ( kino_compile.ntLine, None, t[1], t.lexer.lineno )
   

def p_declaration(t):
   '''declaration : type IDENTIFIER EQ expression
                  | type IDENTIFIER'''
   t[0] = kino_compile.Tree_Node ( kino_compile.ntDeclaration, [t[1], t[4]], t[2], t.lexer.lineno )

def p_assignment(t):
   '''assignment : IDENTIFIER EQ expression'''
   t[0] = kino_compile.Tree_Node ( kino_compile.ntAssignment, [t[3]], t[1], t.lexer.lineno )

def p_primative(t):
   '''expression : expression primative_op expression'''
   t[0] = kino_compile.Tree_Node ( kino_compile.ntPrimative, [t[1], t[3]], t[2], t.lexer.lineno )

def p_primative_unary(t):
   '''expression : unary_op expression'''
   t[0] = kino_compile.Tree_Node ( kino_compile.ntUnaryPrimative, [t[2]], t[1], t.lexer.lineno )
   
def p_primative_unary_op(t):
   '''unary_op : DEREF'''
   t[0] = kino_compile.Tree_Node ( kino_compile.ntUnaryPrimative_op, None, t[1], t.lexer.lineno )

def p_primative_op(t):
   '''primative_op : PLUS
             | MINUS
             | MULT
             | EQV
             | OR
             | AND
             | NEQV'''
   t[0] = kino_compile.Tree_Node ( kino_compile.ntPrimative_op, None, t[1], t.lexer.lineno )
   
def p_expression_number(t):
   '''expression : NUMBER'''
   t[0] = kino_compile.Tree_Node ( kino_compile.ntNumber, None, t[1], t.lexer.lineno )

def p_expression_identifier(t):
   '''expression : IDENTIFIER'''
   t[0] = kino_compile.Tree_Node ( kino_compile.ntIdentifier, None, t[1], t.lexer.lineno )

   
def p_control ( t ):
   '''control : loop
               | conditional'''
   t[0] = kino_compile.Tree_Node ( kino_compile.ntControl, None, t[1], t.lexer.lineno )

def p_conditional(t):
   '''conditional : IF LPAREN expression RPAREN LBRACE program RBRACE ELSE LBRACE program RBRACE'''
   t[0] = kino_compile.Tree_Node ( kino_compile.ntConditional, [t[6], t[10]], t[3], t.lexer.lineno  )

def p_loop ( t ):
   '''loop : WHILE LPAREN expression RPAREN LBRACE program RBRACE'''
   t[0] = kino_compile.Tree_Node ( kino_compile.ntLoop, [t[6]], t[3], t.lexer.lineno )
   

def p_wait_primative ( t ):
   '''wait : WAIT LPAREN NUMBER RPAREN'''
   t[0] = kino_compile.Tree_Node ( kino_compile.ntWait, None, t[3], t.lexer.lineno )
   
def p_type_( t ):
   '''type : INT 
         | LEDR 
         | LEDG
         | SWITCH'''
   t[0] = kino_compile.Tree_Node ( kino_compile.ntType, None, t[1], t.lexer.lineno )
   
def p_parameters ( t ):
   '''parameters : declaration 
                  | declaration parameters'''
   if ( len ( t ) == 2 ):
      t[0] = kino_compile.Tree_Node ( kino_compile.ntParameters, None, t[1], t.lexer.lineno )
   else:
      t[0] = kino_compile.Tree_Node ( kino_compile.ntParameters, [t[2]], t[1], t.lexer.lineno )
      
def p_arguments ( t ):
   '''arguments : expression
                  | expression arguments'''
   if ( len ( t ) == 2 ):
      t[0] = kino_compile.Tree_Node ( kino_compile.ntArguments, None, t[1], t.lexer.lineno )
   else:
      t[0] = kino_compile.Tree_Node ( kino_compile.ntArguments, [t[2]], t[1], t.lexer.lineno )
      
def main_func():
   parser = yacc.yacc()
   s = ""
   s = sys.stdin.read()
   parser.parse(s)


main_func()
