# ============================================================
# TEST ONLY — Exercise A.1 putpixel (red screen)
# Pehle yeh chalao. Poori screen RED honi chahiye.
# Phir full t1a.asm pe jao.
# Bitmap: Connect to label "display" address
# ============================================================
.data
display: .space 65536
colors:
    .word 0x000000
    .word 0xFF0000          # index 1 = Red
    .word 0x00FF00
resx: .word 64
resy: .word 64
stack: .space 100

.text
main:
    la   t0, stack
    addi sp, t0, 100

    lw   s2, resx
    li   s1, 0              # row
rloop:
    li   s0, 0              # col
cloop:
    mv   a0, s1
    mv   a1, s0
    li   a2, 1              # color index = 1 (red)
    jal  ra, putpixel
    addi s0, s0, 1
    blt  s0, s2, cloop
    addi s1, s1, 1
    blt  s1, s2, rloop
    li   a7, 10
    ecall

putpixel:
    lw   t0, resx
    mul  t1, a0, t0
    add  t1, t1, a1
    slli t1, t1, 2
    la   t0, display
    add  t0, t0, t1
    la   t2, colors
    slli t3, a2, 2
    add  t2, t2, t3
    lw   t2, 0(t2)
    sw   t2, 0(t0)
    ret
