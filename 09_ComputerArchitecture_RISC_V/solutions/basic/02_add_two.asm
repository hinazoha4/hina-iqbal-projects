# ============================================================
# LESSON 2 — Do numbers ka sum
# Idea:
#   pehla number -> t0
#   doosra number -> t1
#   sum = t0 + t1 -> t2
# ============================================================

.data
ask1: .asciz "Pehla number: "
ask2: .asciz "Doosra number: "
ans:  .asciz "Sum = "
endl: .asciz "\n"

.text
.globl main
main:
    la   a0, ask1
    li   a7, 4
    ecall
    li   a7, 5
    ecall
    mv   t0, a0            # t0 = pehla

    la   a0, ask2
    li   a7, 4
    ecall
    li   a7, 5
    ecall
    mv   t1, a0            # t1 = doosra

    add  t2, t0, t1        # t2 = t0 + t1

    la   a0, ans
    li   a7, 4
    ecall
    mv   a0, t2
    li   a7, 1
    ecall
    la   a0, endl
    li   a7, 4
    ecall

    li   a7, 10
    ecall
