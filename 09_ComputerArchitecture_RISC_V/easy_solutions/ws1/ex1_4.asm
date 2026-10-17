# Ex 1.4 - Easy
# N se chhotay saare primes print

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

    li   s1, 2               # candidate
outer:
    bge  s1, s0, bye

    li   t0, 2               # d
check:
    mul  t1, t0, t0
    blt  s1, t1, prime       # d*d > n => prime
    rem  t2, s1, t0
    beq  t2, x0, notp
    addi t0, t0, 1
    j    check

prime:
    mv   a0, s1
    li   a7, 1
    ecall
    la   a0, space
    li   a7, 4
    ecall
notp:
    addi s1, s1, 1
    j    outer

bye:
    la   a0, endl
    li   a7, 4
    ecall
    li   a7, 10
    ecall
