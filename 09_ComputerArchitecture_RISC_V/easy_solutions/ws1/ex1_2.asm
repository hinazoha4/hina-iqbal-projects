# Ex 1.2 - Easy
# Numbers jodte raho, 0 aaye to sum print

.data
ask:  .asciz "Number (0=stop): "
ans:  .asciz "Sum = "
endl: .asciz "\n"

.text
.globl main
main:
    li   s0, 0               # sum = 0

loop:
    la   a0, ask
    li   a7, 4
    ecall
    li   a7, 5
    ecall
    beq  a0, x0, done        # 0? stop
    add  s0, s0, a0
    j    loop

done:
    la   a0, ans
    li   a7, 4
    ecall
    mv   a0, s0
    li   a7, 1
    ecall
    la   a0, endl
    li   a7, 4
    ecall
    li   a7, 10
    ecall
