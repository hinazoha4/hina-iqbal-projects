# Ex 1.5 - Easy
# Recursive Fibonacci: fib(i) print jab tak <= N

.data
ask:   .asciz "N: "
space: .asciz " "
endl:  .asciz "\n"

.text
.globl main
main:
    la   a0, ask
    li   a7, 4
    ecall
    li   a7, 5
    ecall
    mv   s0, a0              # N

    li   s1, 0               # i
loop:
    mv   a0, s1
    jal  ra, fib
    mv   t0, a0
    blt  s0, t0, bye         # fib(i) > N
    mv   a0, t0
    li   a7, 1
    ecall
    la   a0, space
    li   a7, 4
    ecall
    addi s1, s1, 1
    j    loop

bye:
    la   a0, endl
    li   a7, 4
    ecall
    li   a7, 10
    ecall

# fib(n): a0 in/out
fib:
    addi sp, sp, -16
    sw   ra, 12(sp)
    sw   s2, 8(sp)
    mv   s2, a0
    beq  s2, x0, z
    li   t0, 1
    beq  s2, t0, o
    addi a0, s2, -1
    jal  ra, fib
    sw   a0, 4(sp)
    addi a0, s2, -2
    jal  ra, fib
    lw   t1, 4(sp)
    add  a0, a0, t1
    j    r
z:  li   a0, 0
    j    r
o:  li   a0, 1
r:  lw   ra, 12(sp)
    lw   s2, 8(sp)
    addi sp, sp, 16
    ret
