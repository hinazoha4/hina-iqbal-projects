# ============================================================
# DAY 1 / LAB SHOW — sirf putpixel (Exercise A.1)
# Prof ko YEHI dikhao aaj: poori screen RED

# Bitmap: Connect to label "display"
# ============================================================
.data
display: .space 65536
colors:
    .word 0x000000   # 0 black
    .word 0xFF0000   # 1 red
    .word 0x00FF00   # 2 green
    .word 0x0000FF   # 3 blue
    .word 0xFFFF00   # 4 yellow   ? naya
    .word 0xFFFFFF   # 5 white    ? naya
resx: .word 64
resy: .word 64
stack: .space 100

.text
.globl main
main:
    la   t0, stack
    addi sp, t0, 100

    lw   s2, resx
    li   s1, 0                 # row
rloop:
    li   s0, 0                 # col
cloop:
    mv   a0, s1                # row
    mv   a1, s0                # col
    li   a2, 1                 # color index = RED
    jal  ra, putpixel
    addi s0, s0, 1
    blt  s0, s2, cloop
    addi s1, s1, 1
    blt  s1, s2, rloop

    li   a7, 10
    ecall

# a0=row a1=col a2=colorIndex
putpixel:
    lw   t0, resx
    mul  t1, a0, t0            # row * cols
    add  t1, t1, a1            # + col
    slli t1, t1, 2             # * 4 bytes
    la   t0, display
    add  t0, t0, t1
    la   t2, colors
    slli t3, a2, 2
    add  t2, t2, t3
    lw   t2, 0(t2)
    sw   t2, 0(t0)
    ret
