# Exercise 1.7
# Tower of Hanoi: ask for number of disks, print move sequence.
# hanoi(n, from, to, aux): move n disks from -> to using aux

.data
prompt:  .asciz "Enter number of disks: "
move1:   .asciz "Move disk from peg "
move2:   .asciz " to peg "
newline: .asciz "\n"

.text
.globl main
main:
    la   a0, prompt
    li   a7, 4
    ecall
    li   a7, 5
    ecall
    mv   s0, a0             # n

    # hanoi(n, from=1, to=3, aux=2)
    mv   a0, s0
    li   a1, 1
    li   a2, 3
    li   a3, 2
    jal  ra, hanoi

    li   a7, 10
    ecall

# void hanoi(n, from, to, aux)
# a0=n, a1=from, a2=to, a3=aux
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
    beq  s0, t0, base_case

    # hanoi(n-1, from, aux, to)
    addi a0, s0, -1
    mv   a1, s1
    mv   a2, s3
    mv   a3, s2
    jal  ra, hanoi

    # print move from -> to
    jal  ra, print_move

    # hanoi(n-1, aux, to, from)
    addi a0, s0, -1
    mv   a1, s3
    mv   a2, s2
    mv   a3, s1
    jal  ra, hanoi
    j    hanoi_done

base_case:
    jal  ra, print_move

hanoi_done:
    lw   ra, 28(sp)
    lw   s0, 24(sp)
    lw   s1, 20(sp)
    lw   s2, 16(sp)
    lw   s3, 12(sp)
    addi sp, sp, 32
    ret

# print using s1=from, s2=to
print_move:
    addi sp, sp, -16
    sw   ra, 12(sp)

    la   a0, move1
    li   a7, 4
    ecall
    mv   a0, s1
    li   a7, 1
    ecall
    la   a0, move2
    li   a7, 4
    ecall
    mv   a0, s2
    li   a7, 1
    ecall
    la   a0, newline
    li   a7, 4
    ecall

    lw   ra, 12(sp)
    addi sp, sp, 16
    ret
