# ============================================================
# EXERCISE 1.7 (BEGINNER) — Tower of Hanoi
#
# Rule:
#   hanoi(n, from, to, aux):
#     if n == 1: print move from->to
#     else:
#       hanoi(n-1, from, aux, to)
#       print move from->to
#       hanoi(n-1, aux, to, from)
#
# Pegs: 1, 2, 3
# ============================================================

.data
ask:  .asciz "Disks kitni? "
m1:   .asciz "Move disk: peg "
m2:   .asciz " -> peg "
endl: .asciz "\n"

.text
.globl main
main:
    la   a0, ask
    li   a7, 4
    ecall
    li   a7, 5
    ecall

    # hanoi(n, 1, 3, 2)
    # a0=n already
    li   a1, 1             # from
    li   a2, 3             # to
    li   a3, 2             # aux
    jal  ra, hanoi

    li   a7, 10
    ecall

# a0=n a1=from a2=to a3=aux
hanoi:
    addi sp, sp, -32
    sw   ra, 28(sp)
    sw   s0, 24(sp)
    sw   s1, 20(sp)
    sw   s2, 16(sp)
    sw   s3, 12(sp)

    mv   s0, a0
    mv   s1, a1
    mv   s2, a2
    mv   s3, a3

    li   t0, 1
    beq  s0, t0, one_disk

    # hanoi(n-1, from, aux, to)
    addi a0, s0, -1
    mv   a1, s1
    mv   a2, s3
    mv   a3, s2
    jal  ra, hanoi

    jal  ra, show_move

    # hanoi(n-1, aux, to, from)
    addi a0, s0, -1
    mv   a1, s3
    mv   a2, s2
    mv   a3, s1
    jal  ra, hanoi
    j    h_done

one_disk:
    jal  ra, show_move

h_done:
    lw   ra, 28(sp)
    lw   s0, 24(sp)
    lw   s1, 20(sp)
    lw   s2, 16(sp)
    lw   s3, 12(sp)
    addi sp, sp, 32
    ret

# print using s1=from, s2=to
show_move:
    la   a0, m1
    li   a7, 4
    ecall
    mv   a0, s1
    li   a7, 1
    ecall
    la   a0, m2
    li   a7, 4
    ecall
    mv   a0, s2
    li   a7, 1
    ecall
    la   a0, endl
    li   a7, 4
    ecall
    ret
