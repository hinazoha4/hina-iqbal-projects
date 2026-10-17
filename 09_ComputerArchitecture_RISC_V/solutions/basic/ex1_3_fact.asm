# ============================================================
# EXERCISE 1.3 (BEGINNER) — Factorial LOOP se
# N! = 1 * 2 * 3 * ... * N
#
# Registers:
#   s0 = N (user)
#   t0 = fact (answer), start 1
#   t1 = i, start 1
#
# Pseudocode:
#   fact = 1
#   i = 1
#   while i <= N:
#       fact = fact * i
#       i = i + 1
# ============================================================

.data
ask:  .asciz "N likho (>=0): "
ans:  .asciz "Factorial = "
endl: .asciz "\n"

.text
.globl main
main:
    la   a0, ask
    li   a7, 4
    ecall
    li   a7, 5
    ecall
    mv   s0, a0            # s0 = N

    li   t0, 1             # fact = 1
    li   t1, 1             # i = 1

loop:
    # agar i > N to ruk jao  (i > N  <=>  N < i)
    blt  s0, t1, done

    mul  t0, t0, t1        # fact = fact * i
    addi t1, t1, 1         # i = i + 1
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
