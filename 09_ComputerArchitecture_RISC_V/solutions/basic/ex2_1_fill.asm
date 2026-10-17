# ============================================================
# EXERCISE 2.1 (BEGINNER) — Poori screen ek color
#
# PEHLE RARS mein:
#   Tools -> Bitmap Display
#   Width=256 Height=256 Unit=4 Base=0x10040000
#   Connect to Program
#
# Idea: 64*64 = 4096 pixels
# Har pixel = 1 word (4 bytes) color 0x00RRGGBB
# ============================================================

.eqv BASE  0x10040000
.eqv WHITE 0x00FFFFFF
# try: RED 0x00FF0000   GREEN 0x0000FF00

.text
.globl main
main:
    li   t0, BASE          # pointer pehle pixel pe
    li   t1, WHITE         # color
    li   t2, 4096          # kitne pixels

loop:
    beq  t2, x0, done
    sw   t1, 0(t0)         # pixel likho
    addi t0, t0, 4         # next pixel (4 bytes)
    addi t2, t2, -1
    j    loop

done:
    li   a7, 10
    ecall
