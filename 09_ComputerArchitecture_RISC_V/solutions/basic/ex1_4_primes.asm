# ============================================================
# EXERCISE 1.4 (BEGINNER) — N se chhotay prime numbers
#
# Idea:
#   candidate = 2, 3, 4, ... jab tak < N
#   har candidate check: koi divisor 2..sqrt se divide?
#   agar nahi to prime, print
#
# Registers:
#   s0 = N
#   s1 = candidate
#   t0 = d (divisor)
# ============================================================

.data
ask:   .asciz "N likho: "
title: .asciz "Primes < N: "
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
    mv   s0, a0

    la   a0, title
    li   a7, 4
    ecall

    li   s1, 2             # candidate = 2

outer:
    bge  s1, s0, finish    # while candidate < N

    # ---- is_prime(s1)? ----
    li   t0, 2             # d = 2
check:
    mul  t1, t0, t0        # t1 = d*d
    blt  s1, t1, yes_prime # d*d > n => prime

    rem  t2, s1, t0        # n % d
    beq  t2, x0, no_prime  # divide ho gaya => not prime

    addi t0, t0, 1         # d++
    j    check

yes_prime:
    mv   a0, s1
    li   a7, 1
    ecall
    la   a0, space
    li   a7, 4
    ecall

no_prime:
    addi s1, s1, 1
    j    outer

finish:
    la   a0, endl
    li   a7, 4
    ecall
    li   a7, 10
    ecall
