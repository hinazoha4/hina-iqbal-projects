.data 
base: .word 0x10010000
.text
	li t1, 0x10010000
	li t2, 0x00ff0000
	sw t2, 0(t1)
	
	addi t1, t1, 4
	li t3, 0x0ffffff
	sw t3, 0(t1)
	
	addi t1, t1, 4
	li t4, 0x0ffff11
	sw t4, 0(t1)