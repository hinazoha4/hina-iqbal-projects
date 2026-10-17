# Exercise 1.2
# Repeatedly ask for integers and sum them. Stop when user enters 0, then print sum.

.data
prompt:  .asciz "Enter an integer (0 to finish): "
result:  .asciz "Sum = "
newline: .asciz "\n"

.text
.globl main
main:
    li   s0, 0              # sum = 0

loop:
    la   a0, prompt
    li   a7, 4
    ecall

    li   a7, 5              # read_int
    ecall
    beq  a0, x0, finish     # if 0, stop
    add  s0, s0, a0
    j    loop

finish:
    la   a0, result
    li   a7, 4
    ecall

    mv   a0, s0
    li   a7, 1
    ecall

    la   a0, newline
    li   a7, 4
    ecall

    li   a7, 10
    ecall
