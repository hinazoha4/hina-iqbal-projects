# ============================================================
# EXERCISE 1.6 (BEGINNER) — Factorial RECURSIVE
#
# Math:
#   fact(0) = 1
#   fact(n) = n * fact(n-1)
#
# Function:
#   a0 mein n jaata hai
#   a0 mein jawab aata hai
#
# Stack kyun?
#   Call ke baad ra aur n save karna padta hai
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
    mv   s0, a0

    mv   a0, s0
    jal  ra, fact          # call fact(N)
    mv   t0, a0            # save answer

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

# ---------- fact(n) ----------
fact:
    addi sp, sp, -16       # thodi stack lo
    sw   ra, 12(sp)        # return address save
    sw   s1, 8(sp)         # s1 save

    mv   s1, a0            # s1 = n
    beq  s1, x0, base      # if n==0 -> 1

    addi a0, s1, -1        # a0 = n-1
    jal  ra, fact          # a0 = fact(n-1)
    mul  a0, a0, s1        # a0 = n * fact(n-1)
    j    leave

base:
    li   a0, 1

leave:
    lw   ra, 12(sp)
    lw   s1, 8(sp)
    addi sp, sp, 16
    ret
