# Exercise 2.2
# Color gradient on 64x64 display:
#   green increases by 4 along columns (x)
#   red increases by 4 along rows (y)
# blue = 0

.eqv DISPLAY_BASE 0x10040000
.eqv WIDTH  64
.eqv HEIGHT 64

.text
.globl main
main:
    li   s0, DISPLAY_BASE
    li   s1, 0              # row y

row_loop:
    li   t0, HEIGHT
    bge  s1, t0, done

    li   s2, 0              # col x
col_loop:
    li   t0, WIDTH
    bge  s2, t0, next_row

    # red = y * 4  (clamp implicitly by 64*4=256 -> use andi 0xFF if needed)
    slli t1, s1, 2          # red
    andi t1, t1, 255
    # green = x * 4
    slli t2, s2, 2
    andi t2, t2, 255
    # color = (red << 16) | (green << 8)
    slli t1, t1, 16
    slli t2, t2, 8
    or   t3, t1, t2

    # address = base + 4*(y*64 + x)
    slli t4, s1, 6          # y*64
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
