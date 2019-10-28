main:
	ori $a0, $zero, 6 #Number of values in array
	ori $a1, $zero, 1000 #Input address
	ori $a2, $zero, 2000 #Output address

	ori $t0, $zero, 8 #Make t0 8
	sw	$t0, 0($a1)	#store 8 into memory
	ori $t0, $zero, 11
	sw	$t0, 4($a1)
	ori $t0, $zero, 11
	sw	$t0, 8($a1)
	ori $t0, $zero, 6
	sw	$t0, 12($a1)
	ori $t0, $zero, 3
	sw	$t0, 16($a1)
	ori $t0, $zero, 20
	sw	$t0, 20($a1)

add_to_output:
	addi $t0, $zero, 1 #loop index
	addi $t1, $a1, 0 #current input address
	addi $t2, $a2, 0 #current output address
	lw $s0, 0($t1) #load first value
	sw $s0, 0($t2) #store first value in output address
	
outputloop:
	addi $t0, $t0, 1
	addi $t1, $t1, 4
	addi $t2, $t2, 4
	lw $s0, 0($t1)
	sw $s0, 0($t2)
	
	blt $t0, $a0, outputloop
	
	
bubble:
	addi $t5, $zero, 1 #loop index t5
repeater:
	addi $t6, $zero, 1 #loop index t6
	addi $t1, $a2, 0 #first input address
	addi $t2, $a2, 4 #second input address
inner_loop:

	lw $t3, 0($t1) #load value from t1 to t3
	lw $t4, 0($t2) #load value from t2 to t1
	
	blt $t3, $t4, noswap
	ori $s10, $t4, 0
	ori $t4, $t3, 0
	ori $t3, $s10, 0
	sw $t3, 0($t1)
	sw $t4, 0($t2)
	
noswap:
	addi $t1, $t1, 4
	addi $t2, $t2, 4
	
	addi $t6, $t6, 1 #increment t6
	bne $t6, $a0, inner_loop
	
	addi $t5, $t5, 1 #increment t5
	bne $t5, $a0, repeater
	
read_values:
	addi $t0, $zero, 0
	addi $t1, $a2, 0 #t1 is output address
	
read_loop:
	lw $s0, 0($t1)
	addi $t1, $t1, 4 #increment output address
	addi $t0, $t0, 1 #increment index value
	bne $t0, $a0, read_loop

halt:
	jal $ra, halt
	