main:
	ori $a0, $zero, 7 #Number of values in array
	ori $a1, $zero, 1000 #Input address
	ori $a2, $zero, 2000 #Output address

	ori $t0, $zero, 8 #Make t0 8
	sw	$t0, 0($a1)	#store 8 into memory
	ori $t0, $zero, 11
	sw	$t0, 4($a1)
	ori $t0, $zero, -11
	sw	$t0, 8($a1)
	ori $t0, $zero, 6
	sw	$t0, 12($a1)
	ori $t0, $zero, -18
	sw	$t0, 16($a1)
	ori $t0, $zero, 22
	sw	$t0, 20($a1)
	ori $t0, $zero, 0
	sw	$t0, 24($a1)

	jal $ra, min
	jal $ra, max
	jal $ra, avg
halt:
	jal $ra, halt
	
min:
	lw $s0, 0($a1) #s0 min
	addi $t3, $a1, 0 #t3 current address
	addi $t0, $zero, 1

minloop:
	addi $t0, $t0, 1 #t0 loop count
	addi $t3, $t3, 4 #current address
	lw $t1, 0($t3)	#load current value into t1
	
	slt $t2, $s0, $t1 #if statement in t2 s0 < t1
	bne $zero, $t2, minendif #if s0 less than t1 jump
	ori $s0, $t1, 0 #else statement
minendif:
	bne $t0, $a0, minloop #looping branch
	sw $s0, 0($a2)	#Save min
	jr $ra	#return
	
max:
    lw $s1, 0($a1) #$s1 max
    addi $t6, $a1, 0
    addi $t0, $zero, 1

maxloop:
    addi $t0, $t0, 1 #t0 loop count
    addi $t6, $t6, 4 #current address
    lw $t4, 0($t6)

    slt $t5, $s1, $t4  #if statement in t5 s1 < t4
    beq $zero, $t5, maxendif
    ori $s1, $t4, 0
maxendif:
    bne $t0, $a0, maxloop
    sw $s1, 0($a2) #save max
	jr $ra	#return
	
avg:
    lw $s2, 0($a1)
    addi $t3, $a1, 0
    addi $t0, $zero, 1
    addi $t1, $s2, 0 #initial sum

avgloop:
    	addi $t0, $t0, 1 #t0 loop count
	addi $t3, $t3, 4 #current address
	lw $t2, 0($t3)	#load current value into t2
	add $t1, $t2, $t1
	div $t4, $t1, $t0
	beq $t4, $t4, avgend
avgend:
	bne $t0, $a0, avgloop
	sw $t4, 0($a2)
	jr $ra  #return
	
	
