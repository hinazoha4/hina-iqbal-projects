# ============================================================
# EXERCISE 2.2 (BEGINNER) — Gradient
# row (y) badhe to RED +4
# col (x) badhe to GREEN +4
# ============================================================

.eqv BASE 0x10040000

.text
.globl main
main:
    li   s0, BASE
    li   s1, 0             # y = 0

row:
    li   t0, 64
    bge  s1, t0, done
    li   s2, 0             # x = 0
col:
    bge  s2, t0, next_y

    # red = y*4 , green = x*4
    slli t1, s1, 2
    andi t1, t1, 255
    slli t2, s2, 2
    andi t2, t2, 255
    slli t1, t1, 16        # red bits
    slli t2, t2, 8         # green bits
    or   t3, t1, t2        # color

    # addr = BASE + 4*(y*64 + x)
    slli t4, s1, 6
    add  t4, t4, s2
    slli t4, t4, 2
    add  t4, t4, s0
    sw   t3, 0(t4)

    addi s2, s2, 1
    j    col
next_y:
    addi s1, s1, 1
    j    row
done:
    li   a7, 10
    ecall
