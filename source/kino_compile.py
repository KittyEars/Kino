import kino_env
import sys
ntControl = 'Control'
ntPrimative = 'Primative'
ntPrimative_op = 'Primative_op'
ntConditional = 'Conditional'
ntLoop = 'Loop'
ntNumber = 'Number'
ntAssignment = 'Assignment'
ntDeclaration = 'Declaration'
ntIdentifier = 'Identifier'
ntLine = 'Line'
ntProgram = 'Program'
ntFunctionDecl = 'Function_Decl'
ntFunctionCall = 'Function_Call'
ntParameters = 'Parameters'
ntArguments = 'Arguments'

label_count = 0

class Tree_Node:
	def __init__(self,type,children, leaf, linenumber):
		self.type = type
		self.linenumber = linenumber
		if children:
			self.children = children
		else:
			self.children = [ ]
		self.leaf = leaf
		
def compile ( node, env, stackcount ):
	global label_count
	if ( node.type == ntPrimative ):
		#print ( ntPrimative )
		rval = compile ( node.children[0], env, stackcount+4 )
		lval = compile ( node.children[1], env, stackcount+8 )
		
		#right side
		if ( rval[0] == ntPrimative ):
			print ( 'lw $v0, %s($zero)' % str(stackcount+4) )
		elif ( rval[0] == ntNumber ):
			print ( 'addi $v0, $zero, %s' % str(rval[1]) )
		elif ( rval[0] == ntIdentifier ):
			print ( 'lw $v0, %s($zero)' % str(rval[1]) )
		
		#left side
		if ( lval[0] == ntPrimative ):
			print ( 'lw $v1, %s($zero)' % str(stackcount+8))
		elif ( lval[0] == ntNumber ):
			print ( 'addi $v1, $zero, %s' % str(lval[1]))
		elif ( lval[0] == ntIdentifier ):
			print ( 'lw $v1, %s($zero)' % str(lval[1]))
		
		if ( node.leaf.leaf == '+' ):
			print ( 'add $v0, $v0, $v1' )
		elif ( node.leaf.leaf == '-' ):
			print ( 'sub $v0, $v0, $v1' )
		
		print ( 'sw $v0, %s($zero)' % stackcount )
		return [ ntPrimative, stackcount]

	elif ( node.type == ntPrimative_op ):
		pass
		
	elif ( node.type == ntConditional ):
		expr_res = compile ( node.leaf, env, stackcount )
		if ( expr_res[0] == ntPrimative ):
			print ( 'lw $v0, %s($zero)' % str ( expr_res[1] )  )
		elif ( expr_res[0] == ntNumber ):
			print ( 'addi $v0, $zero, %s' % str ( expr_res[1] ) )
		elif ( expr_res[0] == ntIdentifier ):
			print ( 'lw $v0, %s($zero)' % str ( expr_res[1] ) )
		print ( 'addi $v1, $zero, 0' )
		print ( 'beq $v1, $v0, label%s' % str (label_count) )
		beq_label = label_count
		label_count = label_count + 1
		compile ( node.children[0], env, stackcount )
		j_label = label_count
		label_count = label_count + 1
		print ( 'j label%s' % j_label )
		compile ( node.children[0], env, stackcount )
		print ( 'label%s:' % beq_label)
		compile ( node.children[1], env, stackcount )
		print ( 'label%s:' % j_label)
		
	elif ( node.type == ntLoop ):
		print ( 'label%s:' % label_count )
		while_begin = label_count
		label_count = label_count + 1
		expr_res = compile ( node.leaf, env, stackcount )
		if ( expr_res[0] == ntPrimative ):
			print ( 'lw $v0, %s($zero)' % str ( expr_res[1] )  )
		elif ( expr_res[0] == ntNumber ):
			print ( 'addi $v0, $zero, %s' % str ( expr_res[1] ) )
		elif ( expr_res[0] == ntIdentifier ):
			print ( 'lw $v0, %s($zero)' % str ( expr_res[1] ) )
		
		print ( 'addi $v1, $zero, 0' )
		print ( 'beq $v1, $v0, label%s' % str (label_count) )
		while_end = label_count
		label_count = label_count + 1
		compile ( node.children[0], env, stackcount )
		print ( 'j label%s' % while_begin )
		print ( 'label%s:' % while_end )
		
	elif ( node.type == ntNumber ):
		return [ ntNumber, node.leaf ]
	elif ( node.type == ntAssignment ):
		try:
			location = kino_env.apply_environment ( env, node.leaf )
		except:
			print ( "Line %s: Unbound identifier %s" % (node.linenumber, node.leaf ) )
			sys.exit ( 0 )
		
		expr_res = compile ( node.children[0], env, stackcount )
		if ( expr_res[0] == ntPrimative ):
			print ( 'lw $v0, %s($zero)' % str ( expr_res[1] )  )
		elif ( expr_res[0] == ntNumber ):
			print ( 'addi $v0, $zero, %s' % str ( expr_res[1] ) )
		elif ( expr_res[0] == ntIdentifier ):
			print ( 'lw $v0, %s($zero)' % str ( expr_res[1] ) )
		print ( 'sw $v0, %s($zero)' % location )

	elif ( node.type == ntIdentifier ):
		#print ( ntIdentifier )
		return [  ntIdentifier ,kino_env.apply_environment ( env, node.leaf ) ]

	elif ( node.type == ntControl ):
		return compile ( node.leaf, env, stackcount )
		
	elif ( node.type == ntLine ):
		return compile ( node.leaf, env, stackcount )

	elif ( node.type == ntProgram ):
		stack_env = compile ( node.leaf, env, stackcount )
		if ( len ( node.children ) > 0 ):
			if ( stack_env != None ):
				compile ( node.children[0], stack_env[0], stack_env[1] )
			else:
				compile ( node.children[0], env, stackcount )
				
	elif ( node.type == ntDeclaration ):
		#print ( ntDeclaration )
		expr_res = compile ( node.children[1], env, stackcount )
		if ( expr_res[0] == ntPrimative ):
			print ( 'lw $v0, %s($zero)' % str ( expr_res[1] )  )
		elif ( expr_res[0] == ntNumber ):
			print ( 'addi $v0, $zero, %s' % str ( expr_res[1] ) )
		elif ( expr_res[0] == ntIdentifier ):
			print ( 'lw $v0, %s($zero)' % str ( expr_res[1] ) )

		print ( 'sw $v0, %s($zero)' % stackcount )
		env = kino_env.extend_environment ( [node.leaf], [stackcount], env )
		return [ env, stackcount + 4]
	
	elif ( node.type == ntFunctionDecl ):
		pass
	elif ( node.type == ntFunctionCall ):
		pass
	elif ( node.type == ntArguments ):
		pass
	elif ( node.type == ntParameters ):
		pass

	else:
		print ( "Trapped exception")
		sys.exit ( 0 )
def printtree ( expr ):
	if (expr.leaf != None ):
		print ( "%s: %s Line: %d" % ( expr.type, expr.leaf, expr.linenumber ) )
		#printtree ( expr.leaf )
	for child in expr.children:
		printtree ( child )