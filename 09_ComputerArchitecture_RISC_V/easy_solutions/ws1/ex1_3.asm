# Ex 1.3 - Easy
# Factorial: 1*2*3*...*N  (loop)

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
    mv   s0, a0              # N

    li   t0, 1               # fact
    li   t1, 1               # i

loop:
    blt  s0, t1, done        # i > N?
    mul  t0, t0, t1
    addi t1, t1, 1
    j    loop

done:
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
