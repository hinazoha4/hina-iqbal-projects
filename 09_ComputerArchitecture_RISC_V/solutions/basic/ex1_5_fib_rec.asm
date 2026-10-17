# ============================================================
# EXERCISE 1.5 (BEGINNER) — Recursive Fibonacci print <= N
#
# Simple approach (samajhne ke liye):
#   fib(0)=0, fib(1)=1
#   fib(n)=fib(n-1)+fib(n-2)
#
# Main: i=0,1,2,... jab tak fib(i) <= N, print karo
# ============================================================

.data
ask:   .asciz "N likho: "
title: .asciz "Fibonacci recursive: "
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

    li   s1, 0             # i = 0
loop_i:
    mv   a0, s1
    jal  ra, fib           # a0 = fib(i)
    mv   t0, a0

    blt  s0, t0, stop      # agar fib(i) > N stop

    mv   a0, t0
    li   a7, 1
    ecall
    la   a0, space
    li   a7, 4
    ecall

    addi s1, s1, 1
    j    loop_i

stop:
    la   a0, endl
    li   a7, 4
    ecall
    li   a7, 10
    ecall

# ---------- fib(n) in a0 ----------
fib:
    addi sp, sp, -16
    sw   ra, 12(sp)
    sw   s1, 8(sp)

    mv   s1, a0
    beq  s1, x0, f0
    li   t0, 1
    beq  s1, t0, f1

    addi a0, s1, -1
    jal  ra, fib
    sw   a0, 4(sp)         # save fib(n-1)

    addi a0, s1, -2
    jal  ra, fib
    lw   t1, 4(sp)
    add  a0, a0, t1
    j    fdone

f0:
    li   a0, 0
    j    fdone
f1:
    li   a0, 1
fdone:
    lw   ra, 12(sp)
    lw   s1, 8(sp)
    addi sp, sp, 16
    ret
