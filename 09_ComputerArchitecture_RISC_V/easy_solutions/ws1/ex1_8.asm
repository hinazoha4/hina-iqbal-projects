# Ex 1.8 - Easy
# 352 -> three five two

.data
ask:   .asciz "Number: "
space: .asciz " "
endl:  .asciz "\n"
n0: .asciz "zero"
n1: .asciz "one"
n2: .asciz "two"
n3: .asciz "three"
n4: .asciz "four"
n5: .asciz "five"
n6: .asciz "six"
n7: .asciz "seven"
n8: .asciz "eight"
n9: .asciz "nine"
names: .word n0,n1,n2,n3,n4,n5,n6,n7,n8,n9
buf:   .space 40

.text
.globl main
main:
    la   a0, ask
    li   a7, 4
    ecall
    li   a7, 5
    ecall
    mv   s0, a0

    bne  s0, x0, digs
    la   a0, n0
    li   a7, 4
    ecall
    j    fin

digs:
    la   s2, buf
    li   s1, 0
    li   t3, 10
take:
    beq  s0, x0, pr
    rem  t0, s0, t3
    div  s0, s0, t3
    slli t1, s1, 2
    add  t1, s2, t1
    sw   t0, 0(t1)
    addi s1, s1, 1
    j    take

pr:
    addi s3, s1, -1
one:
    blt  s3, x0, fin
    slli t1, s3, 2
    add  t1, s2, t1
    lw   t0, 0(t1)
    la   t2, names
    slli t0, t0, 2
    add  t2, t2, t0
    lw   a0, 0(t2)
    li   a7, 4
    ecall
    la   a0, space
    li   a7, 4
    ecall
    addi s3, s3, -1
    j    one

fin:
    la   a0, endl
    li   a7, 4
    ecall
    li   a7, 10
    ecall
