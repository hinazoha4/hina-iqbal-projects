# Ex 2.4 - Easy (simple version)
# Menu:
#   1 = screen clear (color poocho)
#   2 = sine-like demo plot (built-in 64 values)
#   0 = exit
# Full file-plot version baad mein; pehle yeh samjho.
# Bitmap base 0x10040000, Connect!

.eqv BASE 0x10040000

.data
menu: .asciz "1=clear  2=plot demo  0=exit : "
askr: .asciz "R: "
askg: .asciz "G: "
askb: .asciz "B: "
vals: .word 0,4,8,12,16,20,24,28,30,28,24,20,16,12,8,4
      .word 0,-4,-8,-12,-16,-20,-24,-28,-30,-28,-24,-20,-16,-12,-8,-4
      .word 0,5,10,15,20,25,20,15,10,5,0,-5,-10,-15,-20,-25
      .word -20,-15,-10,-5,0,6,12,18,24,18,12,6,0,-6,-12,-18

.text
.globl main
main:
menu_loop:
    la   a0, menu
    li   a7, 4
    ecall
    li   a7, 5
    ecall
    beq  a0, x0, exit
    li   t0, 1
    beq  a0, t0, do_clear
    li   t0, 2
    beq  a0, t0, do_plot
    j    menu_loop

do_clear:
    jal  ra, read_rgb        # s0,s1,s2 = R,G,B
    jal  ra, clear
    jal  ra, axis
    j    menu_loop

do_plot:
    jal  ra, read_rgb
    jal  ra, axis
    la   a0, vals
    jal  ra, plot
    j    menu_loop

exit:
    li   a7, 10
    ecall

read_rgb:
    la   a0, askr
    li   a7, 4
    ecall
    li   a7, 5
    ecall
    mv   s0, a0
    la   a0, askg
    li   a7, 4
    ecall
    li   a7, 5
    ecall
    mv   s1, a0
    la   a0, askb
    li   a7, 4
    ecall
    li   a7, 5
    ecall
    mv   s2, a0
    ret

# clear using s0,s1,s2
clear:
    li   t0, BASE
    andi t1, s0, 255
    andi t2, s1, 255
    andi t3, s2, 255
    slli t1, t1, 16
    slli t2, t2, 8
    or   t1, t1, t2
    or   t1, t1, t3
    li   t4, 4096
c1:
    beq  t4, x0, cdone
    sw   t1, 0(t0)
    addi t0, t0, 4
    addi t4, t4, -1
    j    c1
cdone:
    ret

# black horizontal line at row 32
axis:
    li   t0, 0
a1:
    li   t1, 64
    bge  t0, t1, adone
    # addr = BASE + 4*(32*64 + x)
    li   t2, 2048            # 32*64
    add  t2, t2, t0
    slli t2, t2, 2
    li   t3, BASE
    add  t2, t2, t3
    sw   x0, 0(t2)           # black
    addi t0, t0, 1
    j    a1
adone:
    ret

# plot array a0, color s0,s1,s2
# row = 32 - value, col = i
plot:
    mv   t6, a0
    andi t3, s0, 255
    andi t4, s1, 255
    andi t5, s2, 255
    slli t3, t3, 16
    slli t4, t4, 8
    or   t3, t3, t4
    or   t3, t3, t5          # color word
    li   t0, 0               # i
p1:
    li   t1, 64
    bge  t0, t1, pdone
    slli t2, t0, 2
    add  t2, t6, t2
    lw   t2, 0(t2)           # value
    li   t1, 32
    sub  t1, t1, t2          # row
    # bounds
    blt  t1, x0, pnext
    li   t2, 64
    bge  t1, t2, pnext
    slli t2, t1, 6
    add  t2, t2, t0
    slli t2, t2, 2
    li   t4, BASE
    add  t2, t2, t4
    sw   t3, 0(t2)
pnext:
    addi t0, t0, 1
    j    p1
pdone:
    ret
