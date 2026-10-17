# Ex 1.7 - Easy
# Tower of Hanoi moves print

.data
ask:  .asciz "Disks: "
m1:   .asciz "Move "
m2:   .asciz " -> "
endl: .asciz "\n"

.text
.globl main
main:
    la   a0, ask
    li   a7, 4
    ecall
    li   a7, 5
    ecall
    li   a1, 1               # from peg 1
    li   a2, 3               # to peg 3
    li   a3, 2               # aux peg 2
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
    beq  s0, t0, one

    addi a0, s0, -1
    mv   a1, s1
    mv   a2, s3
    mv   a3, s2
    jal  ra, hanoi
    jal  ra, show
    addi a0, s0, -1
    mv   a1, s3
    mv   a2, s2
    mv   a3, s1
    jal  ra, hanoi
    j    endh
one:
    jal  ra, show
endh:
    lw   ra, 28(sp)
    lw   s0, 24(sp)
    lw   s1, 20(sp)
    lw   s2, 16(sp)
    lw   s3, 12(sp)
    addi sp, sp, 32
    ret

show:
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
