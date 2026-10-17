# Ex 2.3 - Easy
# Bahar BLUE, beech square (center 32,32 side 20) pe gradient
# Square: x,y from 22 to 41

.eqv BASE 0x10040000
.eqv BLUE 0x000000FF

.text
.globl main
main:
    li   s0, BASE
    li   s1, 0
row:
    li   t0, 64
    bge  s1, t0, bye
    li   s2, 0
col:
    bge  s2, t0, ny

    # andar square? 22..41
    li   t1, 22
    blt  s2, t1, out
    blt  s1, t1, out
    li   t1, 41
    blt  t1, s2, out
    blt  t1, s1, out

    # gradient
    slli t2, s1, 2
    andi t2, t2, 255
    slli t3, s2, 2
    andi t3, t3, 255
    slli t2, t2, 16
    slli t3, t3, 8
    or   t4, t2, t3
    j    put
out:
    li   t4, BLUE
put:
    slli t5, s1, 6
    add  t5, t5, s2
    slli t5, t5, 2
    add  t5, t5, s0
    sw   t4, 0(t5)
    addi s2, s2, 1
    j    col
ny:
    addi s1, s1, 1
    j    row
bye:
    li   a7, 10
    ecall
