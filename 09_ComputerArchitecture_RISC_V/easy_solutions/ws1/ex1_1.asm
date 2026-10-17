# Ex 1.1 - Easy
# Fibonacci numbers jo N se chhotay ya barabar hon
# Sequence: 0 1 1 2 3 5 ...

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
    mv   s0, a0              # s0 = N

    # print 0
    li   a0, 0
    li   a7, 1
    ecall
    la   a0, space
    li   a7, 4
    ecall

    beq  s0, x0, bye         # N==0 to bas 0

    # print 1
    li   a0, 1
    li   a7, 1
    ecall
    la   a0, space
    li   a7, 4
    ecall

    li   t0, 0               # prev
    li   t1, 1               # curr

loop:
    add  t2, t0, t1          # next
    blt  s0, t2, bye         # next > N? stop
    mv   a0, t2
    li   a7, 1
    ecall
    la   a0, space
    li   a7, 4
    ecall
    mv   t0, t1
    mv   t1, t2
    j    loop

bye:
    la   a0, endl
    li   a7, 4
    ecall
    li   a7, 10
    ecall
