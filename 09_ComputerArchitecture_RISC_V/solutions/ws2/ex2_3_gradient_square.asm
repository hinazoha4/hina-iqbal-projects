# Exercise 2.3
# Exterior: blue. Interior of square centered (32,32) side 20:
# same gradient as 2.2 (green +=4 along cols, red +=4 along rows).
# Square: x in [22,41], y in [22,41]  (center 32, half-side 10)

.eqv DISPLAY_BASE 0x10040000
.eqv WIDTH  64
.eqv HEIGHT 64
.eqv COLOR_BLUE 0x000000FF
.eqv SQ_MIN 22
.eqv SQ_MAX 41

.text
.globl main
main:
    li   s0, DISPLAY_BASE
    li   s1, 0              # y

row_loop:
    li   t0, HEIGHT
    bge  s1, t0, done
    li   s2, 0              # x

col_loop:
    li   t0, WIDTH
    bge  s2, t0, next_row

    # Check if inside square
    li   t0, SQ_MIN
    blt  s2, t0, outside
    blt  s1, t0, outside
    li   t0, SQ_MAX
    blt  t0, s2, outside
    blt  t0, s1, outside

    # inside: gradient
    slli t1, s1, 2
    andi t1, t1, 255
    slli t2, s2, 2
    andi t2, t2, 255
    slli t1, t1, 16
    slli t2, t2, 8
    or   t3, t1, t2
    j    store

outside:
    li   t3, COLOR_BLUE

store:
    slli t4, s1, 6
    add  t4, t4, s2
    slli t4, t4, 2
    add  t4, t4, s0
    sw   t3, 0(t4)

    addi s2, s2, 1
    j    col_loop

next_row:
    addi s1, s1, 1
    j    row_loop

done:
    li   a7, 10
    ecall
