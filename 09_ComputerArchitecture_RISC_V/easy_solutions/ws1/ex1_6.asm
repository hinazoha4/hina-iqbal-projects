# Ex 1.6 - Easy
# Recursive factorial: fact(n) = n * fact(n-1)

.data
ask:  .asciz "N: "
ans:  .asciz "N! = "
endl: .asciz "\n"

.text
.globl main
main:
    la   a0, ask
    li   a7, 4
    ecall
    li   a7, 5
    ecall
    jal  ra, fact
    mv   t0, a0

    la   a0, ans
    li   a7, 4
    ecall
    mv   a0, t0
    li   a7, 1
    ecall
    la   a0, endl
    li   a7, 4
    ecall
    li   a7, 10
    ecall

fact:
    addi sp, sp, -16
    sw   ra, 12(sp)
    sw   s1, 8(sp)
    mv   s1, a0
    beq  s1, x0, base
    addi a0, s1, -1
    jal  ra, fact
    mul  a0, a0, s1
    j    leave
base:
    li   a0, 1
leave:
    lw   ra, 12(sp)
    lw   s1, 8(sp)
    addi sp, sp, 16
    ret
