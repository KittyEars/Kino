.text
addi $v0, $zero, 0
sw $v0, 4($zero)
addi $v0, $zero, 0
sw $v0, 32($zero)
label0:
addi $v0, $zero, 1
addi $v1, $zero, 0
beq $v1, $v0, label1
lw $v0, 32($zero)
addi $v1, $zero, 5
sub $v0, $v0, $v1
sw $v0, 36($zero)
lw $v0, 36($zero)
addi $v1, $zero, 0
beq $v1, $v0, label2
lw $v0, 32($zero)
addi $v1, $zero, 1
add $v0, $v0, $v1
sw $v0, 36($zero)
lw $v0, 36($zero)
sw $v0, 32($zero)
j label3
lw $v0, 32($zero)
addi $v1, $zero, 1
add $v0, $v0, $v1
sw $v0, 36($zero)
lw $v0, 36($zero)
sw $v0, 32($zero)
label2:
addi $v0, $zero, 0
sw $v0, 32($zero)
label3:
lw $v0, 32($zero)
sw $v0, 4($zero)
addi $a0, $zero, 0
lui $a0, 254
addi $a0, $a0, 20522
addi $v0, $zero, 0
wait4:
addi $v0, $v0, 1
bne $v0, $a0, wait4
j label0
label1:
