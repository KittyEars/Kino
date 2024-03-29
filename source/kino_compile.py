import kino_env
import sys
import operator #thats not the way it feels
import math
ntControl = 'Control'
ntPrimative = 'Primative'
ntPrimative_op = 'Primative_op'
ntUnaryPrimative = 'UnaryPrimative'
ntUnaryPrimative_op = 'UnaryPrimative_op'
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
ntType = 'Type'
ntWait = 'Wait'

label_count = 0
time_constant = 60 * math.pow(10,-9)
class Tree_Node:
   def __init__(self,type,children, leaf, linenumber):
      self.type = type
      self.linenumber = linenumber
      if children:
         self.children = children
      else:
         self.children = [ ]
      self.leaf = leaf
primative_op_dict = { "+" : operator.add, "-" : operator.sub, 
                 "*" : operator.mul, "==" : operator.xor, 
                 "!=" : operator.sub }
                 
def compile ( node, env, stackcount ):
   global label_count
   if ( node.type == ntUnaryPrimative ):
      rval = compile ( node.children[0], env, stackcount + 4 )
      #right side
      if ( rval[0] == ntPrimative ):
         print ( 'lw $v0, %s($zero)' % str(stackcount+4) )
      elif ( rval[0] == ntNumber ):
         print ( 'addi $v0, $zero, %s' % str(rval[1]) )
      elif ( rval[0] == ntIdentifier ):
         print ( 'lw $v0, %s($zero)' % str(rval[1]) )
      
      print ( 'sw $v0, %s($zero)' % stackcount )
      return [ ntPrimative, stackcount ]
      
   if ( node.type == ntPrimative ):
      #print ( ntPrimative )
      rval = compile ( node.children[0], env, stackcount+4 )
      lval = compile ( node.children[1], env, stackcount+8 )
      
      if ( rval[0] == ntNumber and lval[0] == ntNumber ):
         return [ ntNumber, primative_op_dict[node.leaf.leaf](rval[1], lval[1]) ]
      else:
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
         elif ( node.leaf.leaf == '==' ):
            #todo: This isn't the safest way to do eqv 
            #but it will work for now
            print ( 'xor $v0, $v0, $v1' )
         elif ( node.leaf.leaf == '!=' ):
            #todo: again not the safest way, but given the 
            #number of opcodes and speed this is the best option
            print ( 'sub $v0, $v0, $v1' )
         elif ( node.leaf.leaf == '|' ):
            print ( 'or $v0, $v0, $v1' )
         elif ( node.leaf.leaf == '&' ):
            print ( 'and $v0, $v0, $v1' )
         
         print ( 'sw $v0, %s($zero)' % stackcount )
         return [ ntPrimative, stackcount]

   elif ( node.type == ntPrimative_op ):
      pass
   elif ( node.type == ntWait ):
      loop_count = (int)(node.leaf / time_constant )
      print ( "addi $a0, $zero, 0" )
      if (loop_count < math.pow(2,32)):
         if ( loop_count > math.pow(2,15)): 
            print ( "lui $a0, %s" % str(loop_count >> 16) )
            print ( "addi $a0, $a0, %s" % str(loop_count & 0xFFFF) )
         else:
            print ( "addi $a0, $a0, %s" % str(loop_count & 0xFFFF) )
      else:
         print ( "Compile Error." )
         sys.exit(0)
      print ( "addi $v0, $zero, 0" )
      print ( "wait%s:" % str(label_count) )

      wend = label_count
      label_count = label_count + 1
      print ( "addi $v0, $v0, 1" )
      print ( "bne $v0, $a0, wait%s" % wend )
      
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
      expr_res = compile ( node.children[1], env, stackcount )
      if ( expr_res[0] == ntPrimative ):
         print ( 'lw $v0, %s($zero)' % str ( expr_res[1] )  )
      elif ( expr_res[0] == ntNumber ):
         print ( 'addi $v0, $zero, %s' % str ( expr_res[1] ) )
      elif ( expr_res[0] == ntIdentifier ):
         print ( 'lw $v0, %s($zero)' % str ( expr_res[1] ) )
      
      VarAddr = compile ( node.children[0], env, stackcount ) 
      print ( 'sw $v0, %s($zero)' % VarAddr )

      env = kino_env.extend_environment ( [node.leaf], [VarAddr], env )
      if ( VarAddr < 16 ):
         return [env, stackcount]
      else:
         return [ env, stackcount + 4]
   
      
   elif ( node.type == ntType ):
      if ( node.leaf == 'ledr' ):
         return 4
      elif ( node.leaf == 'ledg' ):
         return 8
      elif ( node.leaf == 'switch' ):
         return 12

      else:
         return stackcount
   else:
      print ( "Trapped exception")
      sys.exit ( 0 )
      
def printtree ( expr ):
   if (expr.leaf != None ):
      print ( "%s: %s Line: %d" % ( expr.type, expr.leaf, expr.linenumber ) )
      #printtree ( expr.leaf )
   for child in expr.children:
      printtree ( child )