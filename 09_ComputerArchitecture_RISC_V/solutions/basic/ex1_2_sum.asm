# ============================================================
# EXERCISE 1.2 (BEGINNER STYLE)
# Numbers lo, jodte raho. 0 aaye to ruk jao, sum print.
#
# Variables (registers):
#   s0 = sum   (important, isliye s0)
#   a0 = har baar naya input
# ============================================================

.data
ask:  .asciz "Number likho (0 = khatam): "
ans:  .asciz "Sum = "
endl: .asciz "\n"

.text
.globl main
main:
    li   s0, 0             # sum = 0

loop:
    # poochho
    la   a0, ask
    li   a7, 4
    ecall

    # padho
    li   a7, 5
    ecall                  # a0 = user number

    # agar a0 == 0 to finish
    beq  a0, x0, finish

    # sum = sum + a0
    add  s0, s0, a0
    j    loop              # wapas loop

finish:
    la   a0, ans
    li   a7, 4
    ecall

    mv   a0, s0            # print sum
    li   a7, 1
    ecall

    la   a0, endl
    li   a7, 4
    ecall

    li   a7, 10
    ecall
