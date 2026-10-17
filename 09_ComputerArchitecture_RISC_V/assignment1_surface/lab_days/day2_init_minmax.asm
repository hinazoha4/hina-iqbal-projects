# ============================================================
# DAY 2 / LAB SHOW — init + proper Min/Max + pixcor
# Prof ne kaha: Min/Max init mein PROPER values
#
# Hum assign karte hain:
#   Minx = Miny = -pi/2
#   Maxx = Maxy = +pi/2
#   pixcorx = (Maxx-Minx)/cols
#   pixcory = (Maxy-Miny)/rows
#
# Test: color index sirf COLUMN se (mapping kaam kar rahi hai)
# Full sin/cos KAL / baad mein
# ============================================================
.data
display: .space 65536
colors:
    .word 0x000000, 0xFF0000, 0x00FF00, 0x0000FF, 0xFFFF00
    .word 0xFF00FF, 0x00FFFF, 0xFFFFFF, 0x808080, 0xFFA500
    .word 0xA52A2A, 0xFF69B4, 0x4682B4, 0x32CD32, 0xFF4500
    .word 0xDA70D6, 0x98FB98, 0xFFC0CB, 0xDDA0DD, 0xB0E0E6
    .word 0x800000, 0x008000, 0x000080, 0x808000, 0x800080
    .word 0x008080, 0xC0C0C0, 0xF0E68C, 0xD2691E, 0xB22222
    .word 0x7FFF00, 0x00FF7F, 0x5F9EA0, 0xDC143C, 0x8B008B
    .word 0x556B2F, 0xFF1493, 0x1E90FF, 0xEEE8AA, 0xAFEEEE
    .word 0xDB7093, 0xFFEFD5, 0xFFDAB9, 0xCD853F, 0x9ACD32
    .word 0x6A5ACD, 0xFF6347, 0x40E0D0, 0xF5DEB3, 0xFFFFFF
# 50 colors (index 0..49)

stack: .space 100

# PROF: proper values yahan AND init mein overwrite/confirm
Maxx: .double 1.5707963267948966   # +pi/2
Maxy: .double 1.5707963267948966
Minx: .double -1.5707963267948966  # -pi/2
Miny: .double -1.5707963267948966

pixcorx: .double 0
pixcory: .double 0
resx: .word 64
resy: .word 64

pi:  .double 3.141592653589793
one: .double 1.0
two: .double 2.0
num49: .double 49.0

.text
.globl main
main:
    la   t0, stack
    addi sp, t0, 100

    jal  ra, init              # <-- Min/Max + pixcor yahan set

    lw   s2, resx
    li   s1, 0
rloop:
    li   s0, 0
cloop:
    # SIMPLE test mapping (bina sin/cos): color ~ column
    # taake dikhe init/domain ke baad screen fill hoti hai
    mv   a0, s1
    mv   a1, s0
    # index = col * 49 / (cols-1)  approx: col % 50 for demo
    mv   t0, s0
    li   t1, 50
    rem  a2, t0, t1
    jal  ra, putpixel

    addi s0, s0, 1
    blt  s0, s2, cloop
    addi s1, s1, 1
    blt  s1, s2, rloop

    li   a7, 10
    ecall

# ----- init: Algorithm 5 (yeh PROF ko explain karo) -----
init:
    # pi/2
    la   t0, pi
    fld  ft0, 0(t0)
    la   t0, two
    fld  ft1, 0(t0)
    fdiv.d ft2, ft0, ft1       # +pi/2

    # -pi/2 = 0 - pi/2
    li   t1, 0
    fcvt.d.w ft3, t1
    fsub.d ft3, ft3, ft2

    # STORE proper Min/Max
    la   t0, Maxx
    fsd  ft2, 0(t0)
    la   t0, Maxy
    fsd  ft2, 0(t0)
    la   t0, Minx
    fsd  ft3, 0(t0)
    la   t0, Miny
    fsd  ft3, 0(t0)

    # pixcorx = (Maxx-Minx)/cols = pi/cols
    lw   t1, resx
    fcvt.d.w ft4, t1
    fsub.d ft5, ft2, ft3
    fdiv.d ft5, ft5, ft4
    la   t0, pixcorx
    fsd  ft5, 0(t0)

    # pixcory = (Maxy-Miny)/rows
    lw   t1, resy
    fcvt.d.w ft4, t1
    fsub.d ft5, ft2, ft3
    fdiv.d ft5, ft5, ft4
    la   t0, pixcory
    fsd  ft5, 0(t0)
    ret

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
