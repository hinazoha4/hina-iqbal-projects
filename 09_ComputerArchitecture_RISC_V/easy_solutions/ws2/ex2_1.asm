# Ex 2.1 - Easy
# Poori Bitmap screen WHITE
# Tools->Bitmap Display: 256x256, unit 4, base 0x10040000, Connect

.eqv BASE  0x10040000
.eqv COLOR 0x00FFFFFF
# change COLOR: red=0x00FF0000 green=0x0000FF00 custom=0x00328040

.text
.globl main
main:
    li   t0, BASE
    li   t1, COLOR
    li   t2, 4096            # 64*64 pixels
loop:
    beq  t2, x0, bye
    sw   t1, 0(t0)
    addi t0, t0, 4
    addi t2, t2, -1
    j    loop
bye:
    li   a7, 10
    ecall
