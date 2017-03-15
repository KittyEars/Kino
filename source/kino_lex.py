import operator
import ply.yacc as yacc
import sys
import ply.lex as lex
import re
tokens = ( 'WORD', 'IDENTIFIER', 'DEREF', 'SEMICOLON', 'NUMBER', 'IF', 'ELSE', 'WHILE', 'INT', 'STRING', 'PLUS', 'MINUS', 'MULT', 'EQV', 'NEQV', 'EQ', 'LBRACE', 'RBRACE', 'LPAREN', 'RPAREN' )

keywords = ( 'if', 'else', 'while', 'int', 'string', 'eqv'  )

keyword_lookup = { 'if' : 'IF', 'else' : 'ELSE', 'while' : 'WHILE', 'int' : 'INT', 'string' : 'STRING' }

t_DEREF		 = r'\&'
t_PLUS    	 = r'\+'
t_MINUS   	 = r'-'
t_MULT    	 = r'\*'
t_EQ		 = r'='
t_EQV 	 	 = r'=='
t_NEQV		 = r'!='
t_LBRACE	 = r'\{'
t_RBRACE	 = r'\}'
t_LPAREN  	 = r'\('
t_RPAREN  	 = r'\)'
t_SEMICOLON  = r';'
t_ignore 	 = " \t"


def t_WORD (t):
	r'[A-Za-z_][A-Za-z_0-9]*'
	pattern = re.compile("^[A-Za-z_][A-Za-z_0-9]*$")
	#if the identifier is a keyword, parse it as such
	if t.value in keywords:
		t.type = keyword_lookup[t.value]
	#otherwise it might be a variable so check that
	elif pattern.match ( t.value ):
		t.type = 'IDENTIFIER'
	#otherwise its a syntax error
	else:
		print ( "%s ERROR" % t.value )
		sys.exit ( -1 )
	return t

def t_NUMBER(t):
	r'\d+'
	#try to convery the string to an int, flag overflows
	try:
		t.value = int (t.value)
	except ValueError:
		
	#	print("Run time error: number too large '%(value)s' '%(lineno)d'" % { value : t.value[0], lineno : t.lexer.lineno }  )
		t.value = 0
	return t

def t_newline(t):
	r'\n+'
	#continue to next line
	t.lexer.lineno += t.value.count ( "\n" )

def t_error(t):
	print ( "Illegal statement %d" % t.lexer.lineno )
	
lexer = lex.lex()

precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'MULT', 'EQ' ),
	('left', 'LBRACE', 'LPAREN' ),
	('left', 'IDENTIFIER' ),
	('right', 'DEREF' )
)