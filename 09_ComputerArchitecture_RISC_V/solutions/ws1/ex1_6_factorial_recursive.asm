# Exercise 1.6
# Factorial computed recursively. fact(n) = n * fact(n-1), fact(0)=1

.data
prompt:  .asciz "Enter a non-negative integer N: "
result:  .asciz "Factorial = "
newline: .asciz "\n"
err_msg: .asciz "Error: N must be >= 0\n"

.text
.globl main
main:
    la   a0, prompt
    li   a7, 4
    ecall
    li   a7, 5
    ecall
    mv   s0, a0
    blt  s0, x0, error

    mv   a0, s0
    jal  ra, fact
    mv   t0, a0             # save result

    la   a0, result
    li   a7, 4
    ecall
    mv   a0, t0
    li   a7, 1
    ecall
    la   a0, newline
    li   a7, 4
    ecall
    j    exit

error:
    la   a0, err_msg
    li   a7, 4
    ecall

exit:
    li   a7, 10
    ecall

# int fact(int n)  — a0 = n, return in a0
fact:
    addi sp, sp, -16
    sw   ra, 12(sp)
    sw   s1, 8(sp)

    mv   s1, a0
    beq  s1, x0, base       # fact(0) = 1

    addi a0, s1, -1
    jal  ra, fact           # a0 = fact(n-1)
    mul  a0, a0, s1         # a0 = n * fact(n-1)
    j    fact_done

base:
    li   a0, 1

fact_done:
    lw   ra, 12(sp)
    lw   s1, 8(sp)
    addi sp, sp, 16
    ret
