# Exercise 1.3
# Prompt for an integer N and print N! (iterative). Assumes N >= 0 and result fits in 32-bit.

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
    mv   s0, a0             # s0 = N

    blt  s0, x0, error

    li   t0, 1              # fact = 1
    li   t1, 1              # i = 1

loop:
    blt  s0, t1, print      # while i <= N
    mul  t0, t0, t1         # fact *= i  (needs M extension; RARS has it)
    addi t1, t1, 1
    j    loop

print:
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
