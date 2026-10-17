# ============================================================
# EXERCISE 1.1 (BEGINNER) — Fibonacci numbers <= N
# Sequence: 0, 1, 1, 2, 3, 5, 8, ... jab tak number <= N
#
# Registers:
#   s0 = N
#   t0 = prev
#   t1 = curr
#   t2 = next = prev + curr
# ============================================================

.data
ask:   .asciz "N likho: "
title: .asciz "Fibonacci (<= N): "
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
    mv   s0, a0            # N

    la   a0, title
    li   a7, 4
    ecall

    # pehle 0 print (agar N >= 0)
    blt  s0, x0, exit
    li   a0, 0
    li   a7, 1
    ecall
    la   a0, space
    li   a7, 4
    ecall

    beq  s0, x0, exit      # sirf 0 chahiye tha

    # phir 1 print
    li   a0, 1
    li   a7, 1
    ecall
    la   a0, space
    li   a7, 4
    ecall

    li   t0, 0             # prev = 0
    li   t1, 1             # curr = 1

next:
    add  t2, t0, t1        # next = prev + curr
    blt  s0, t2, exit      # agar next > N, stop

    # print next
    mv   a0, t2
    li   a7, 1
    ecall
    la   a0, space
    li   a7, 4
    ecall

    mv   t0, t1            # prev = curr
    mv   t1, t2            # curr = next
    j    next

exit:
    la   a0, endl
    li   a7, 4
    ecall
    li   a7, 10
    ecall
