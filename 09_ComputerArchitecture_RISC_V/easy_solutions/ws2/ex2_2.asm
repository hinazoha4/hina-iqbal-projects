# Ex 2.2 - Easy
# Gradient: row pe red+4, column pe green+4
# Bitmap: base 0x10040000, Connect

.eqv BASE 0x10040000

.text
.globl main
main:
    li   s0, BASE
    li   s1, 0               # y
row:
    li   t0, 64
    bge  s1, t0, bye
    li   s2, 0               # x
col:
    bge  s2, t0, ny
    slli t1, s1, 2
    andi t1, t1, 255
    slli t2, s2, 2
    andi t2, t2, 255
    slli t1, t1, 16
    slli t2, t2, 8
    or   t3, t1, t2
    slli t4, s1, 6
    add  t4, t4, s2
    slli t4, t4, 2
    add  t4, t4, s0
    sw   t3, 0(t4)
    addi s2, s2, 1
    j    col
ny:
    addi s1, s1, 1
    j    row
bye:
    li   a7, 10
    ecall
