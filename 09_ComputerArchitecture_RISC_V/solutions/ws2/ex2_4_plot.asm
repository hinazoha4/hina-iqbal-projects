# Exercise 2.4 — Plot sequences on Bitmap Display (64x64)
#
# RARS Bitmap Display settings:
#   Display Width/Height = 256, Unit Width/Height = 4  => 64x64
#   Base address for display = 0x10040000
#   Click "Connect to Program"
#
# Menu:
#   1 = clear screen (ask R,G,B)
#   2 = plot from file (64 lines of +DD / -DD), ask R,G,B
#   3 = square wave (optional)
#   4 = triangle wave (optional)
#   0 = exit

.eqv DISPLAY_BASE 0x10040000
.eqv WIDTH  64
.eqv HEIGHT 64
.eqv AXIS_Y 32

.data
menu:    .asciz "\n1=clear  2=plot file  3=square  4=triangle  0=exit\nChoice: "
ask_r:   .asciz "R (0-255): "
ask_g:   .asciz "G (0-255): "
ask_b:   .asciz "B (0-255): "
ask_file:.asciz "File name: "
err_open:.asciz "Cannot open file\n"
ok_msg:  .asciz "Done.\n"
filename:.space 128
linebuf: .space 8
values:  .word 0:64          # 64 plotted samples
sqbuf:   .word 0:64
tribuf:  .word 0:64

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
    beq  a0, t0, do_plot_file
    li   t0, 3
    beq  a0, t0, do_square
    li   t0, 4
    beq  a0, t0, do_triangle
    j    menu_loop

do_clear:
    jal  ra, read_rgb        # a0=R a1=G a2=B
    jal  ra, clear
    jal  ra, drawaxis
    la   a0, ok_msg
    li   a7, 4
    ecall
    j    menu_loop

do_plot_file:
    la   a0, ask_file
    li   a7, 4
    ecall
    la   a0, filename
    li   a1, 128
    li   a7, 8               # read_string
    ecall
    # strip trailing newline from read_string
    la   t0, filename
strip:
    lbu  t1, 0(t0)
    beq  t1, x0, strip_done
    li   t2, 10
    beq  t1, t2, put_nul
    li   t2, 13
    beq  t1, t2, put_nul
    addi t0, t0, 1
    j    strip
put_nul:
    sb   x0, 0(t0)
strip_done:

    # open file
    la   a0, filename
    li   a1, 0               # read-only
    li   a7, 1024
    ecall
    blt  a0, x0, open_fail
    mv   s7, a0              # fd

    la   s8, values
    li   s9, 0               # count
read_lines:
    li   t0, 64
    bge  s9, t0, close_file

    # read exactly 3 chars + newline into linebuf (or until newline)
    la   t1, linebuf
    li   t2, 0
rd_char:
    li   t3, 4
    bge  t2, t3, parse_line
    mv   a0, s7
    mv   a1, t1
    li   a2, 1
    li   a7, 63              # read
    ecall
    ble  a0, x0, close_file
    lbu  t4, 0(t1)
    li   t5, 10
    beq  t4, t5, parse_line
    li   t5, 13
    beq  t4, t5, rd_char     # skip CR
    addi t1, t1, 1
    addi t2, t2, 1
    j    rd_char

parse_line:
    sb   x0, 0(t1)
    la   a0, linebuf
    jal  ra, asciitoint
    slli t0, s9, 2
    add  t0, s8, t0
    sw   a0, 0(t0)
    addi s9, s9, 1
    j    read_lines

close_file:
    mv   a0, s7
    li   a7, 57
    ecall

    jal  ra, read_rgb
    # keep previous screen; draw axis then plot
    jal  ra, drawaxis
    la   a0, values
    # R,G,B still? read_rgb left them in s0,s1,s2
    mv   a1, s0
    mv   a2, s1
    mv   a3, s2
    jal  ra, plot
    la   a0, ok_msg
    li   a7, 4
    ecall
    j    menu_loop

open_fail:
    la   a0, err_open
    li   a7, 4
    ecall
    j    menu_loop

do_square:
    jal  ra, gen_square
    jal  ra, read_rgb
    jal  ra, drawaxis
    la   a0, sqbuf
    mv   a1, s0
    mv   a2, s1
    mv   a3, s2
    jal  ra, plot
    j    menu_loop

do_triangle:
    jal  ra, gen_triangle
    jal  ra, read_rgb
    jal  ra, drawaxis
    la   a0, tribuf
    mv   a1, s0
    mv   a2, s1
    mv   a3, s2
    jal  ra, plot
    j    menu_loop

exit:
    li   a7, 10
    ecall

# ---------- read_rgb -> s0=R s1=G s2=B ----------
read_rgb:
    addi sp, sp, -4
    sw   ra, 0(sp)
    la   a0, ask_r
    li   a7, 4
    ecall
    li   a7, 5
    ecall
    mv   s0, a0
    la   a0, ask_g
    li   a7, 4
    ecall
    li   a7, 5
    ecall
    mv   s1, a0
    la   a0, ask_b
    li   a7, 4
    ecall
    li   a7, 5
    ecall
    mv   s2, a0
    mv   a0, s0
    mv   a1, s1
    mv   a2, s2
    lw   ra, 0(sp)
    addi sp, sp, 4
    ret

# ---------- asciitoint(char *cval) ----------
# Format: +DD or -DD  (3 chars). Returns signed int in a0.
asciitoint:
    lbu  t0, 0(a0)          # sign
    lbu  t1, 1(a0)          # tens ascii
    lbu  t2, 2(a0)          # ones ascii
    addi t1, t1, -48
    addi t2, t2, -48
    li   t3, 10
    mul  t1, t1, t3
    add  t1, t1, t2         # magnitude
    li   t4, 45             # '-'
    bne  t0, t4, pos
    sub  a0, x0, t1
    ret
pos:
    mv   a0, t1
    ret

# ---------- setpixel(row, col, R, G, B) ----------
# a0=row a1=col a2=R a3=G  |  blue on stack? We use a4 via calling convention:
# For RV32, 5th arg is on stack. Simpler: use s-registers from callers,
# or pack: we'll take blue in t0 via alternate: a0=row a1=col a2=color_word
# Spec asks unsigned red,green,blue — use a0=row a1=col a2=R a3=G and load B from 0(sp) if needed.
# Here: a0=row, a1=col, a2=R, a3=G, and blue passed in t6 by convention for this file,
# OR we use: setpixel_rgb with a0,a1,a2,a3 and s11=B temporarily.
#
# Implementation: a0=row a1=col a2=R a3=G ; blue in s11 (documented).
setpixel:
    # bounds check 0..63
    blt  a0, x0, sp_ret
    blt  a1, x0, sp_ret
    li   t0, 64
    bge  a0, t0, sp_ret
    bge  a1, t0, sp_ret

    andi a2, a2, 255
    andi a3, a3, 255
    andi t1, s11, 255
    slli t2, a2, 16
    slli t3, a3, 8
    or   t2, t2, t3
    or   t2, t2, t1

    slli t0, a0, 6
    add  t0, t0, a1
    slli t0, t0, 2
    li   t1, DISPLAY_BASE
    add  t0, t0, t1
    sw   t2, 0(t0)
sp_ret:
    ret

# ---------- clear(R,G,B) in a0,a1,a2 ----------
clear:
    addi sp, sp, -16
    sw   ra, 12(sp)
    sw   s0, 8(sp)
    sw   s1, 4(sp)
    sw   s2, 0(sp)
    mv   s0, a0
    mv   s1, a1
    mv   s2, a2
    mv   s11, s2            # blue for setpixel
    li   t4, 0              # row
c_row:
    li   t5, 64
    bge  t4, t5, c_done
    li   t6, 0              # col
c_col:
    bge  t6, t5, c_nr
    mv   a0, t4
    mv   a1, t6
    mv   a2, s0
    mv   a3, s1
    # s11 already blue
    sw   t4, -4(sp)         # protect? use stack carefully — t4/t6 not saved across call
    addi sp, sp, -8
    sw   t4, 0(sp)
    sw   t6, 4(sp)
    jal  ra, setpixel
    lw   t4, 0(sp)
    lw   t6, 4(sp)
    addi sp, sp, 8
    addi t6, t6, 1
    j    c_col
c_nr:
    addi t4, t4, 1
    j    c_row
c_done:
    lw   ra, 12(sp)
    lw   s0, 8(sp)
    lw   s1, 4(sp)
    lw   s2, 0(sp)
    addi sp, sp, 16
    ret

# ---------- drawaxis(): horizontal black line at row 32 ----------
drawaxis:
    addi sp, sp, -8
    sw   ra, 4(sp)
    sw   s3, 0(sp)
    li   s11, 0             # blue=0
    li   s3, 0              # col
ax_loop:
    li   t0, 64
    bge  s3, t0, ax_done
    li   a0, AXIS_Y
    mv   a1, s3
    li   a2, 0
    li   a3, 0
    jal  ra, setpixel
    addi s3, s3, 1
    j    ax_loop
ax_done:
    lw   ra, 4(sp)
    lw   s3, 0(sp)
    addi sp, sp, 8
    ret

# ---------- plot(values*, R, G, B) ----------
# a0=ptr a1=R a2=G a3=B
# values[i] in [-31,+32]; plot at row = 32 - value, col = i
plot:
    addi sp, sp, -32
    sw   ra, 28(sp)
    sw   s0, 24(sp)
    sw   s1, 20(sp)
    sw   s2, 16(sp)
    sw   s3, 12(sp)
    sw   s4, 8(sp)

    mv   s0, a0
    mv   s1, a1
    mv   s2, a2
    mv   s3, a3
    mv   s11, s3
    li   s4, 0              # i

p_loop:
    li   t0, 64
    bge  s4, t0, p_done
    slli t1, s4, 2
    add  t1, s0, t1
    lw   t2, 0(t1)          # value
    li   t3, AXIS_Y
    sub  t3, t3, t2         # row = 32 - value

    mv   a0, t3
    mv   a1, s4
    mv   a2, s1
    mv   a3, s2
    jal  ra, setpixel

    addi s4, s4, 1
    j    p_loop
p_done:
    lw   ra, 28(sp)
    lw   s0, 24(sp)
    lw   s1, 20(sp)
    lw   s2, 16(sp)
    lw   s3, 12(sp)
    lw   s4, 8(sp)
    addi sp, sp, 32
    ret

# ---------- optional: square wave ----------
gen_square:
    la   t0, sqbuf
    li   t1, 0
gs:
    li   t2, 64
    bge  t1, t2, gs_done
    andi t3, t1, 8          # period 16: high 8, low 8
    beq  t3, x0, gs_low
    li   t4, 20
    j    gs_st
gs_low:
    li   t4, -20
gs_st:
    slli t5, t1, 2
    add  t5, t0, t5
    sw   t4, 0(t5)
    addi t1, t1, 1
    j    gs
gs_done:
    ret

# ---------- optional: triangle wave ----------
gen_triangle:
    la   t0, tribuf
    li   t1, 0
gt:
    li   t2, 64
    bge  t1, t2, gt_done
    # period 32: rise 0..16 then fall
    andi t3, t1, 31
    li   t4, 16
    blt  t3, t4, gt_up
    li   t5, 32
    sub  t5, t5, t3         # 16..0
    j    gt_val
gt_up:
    mv   t5, t3
gt_val:
    addi t5, t5, -8         # center around 0 roughly (-8..+8)
    slli t6, t5, 1          # scale
    slli t7, t1, 2
    add  t7, t0, t7
    sw   t6, 0(t7)
    addi t1, t1, 1
    j    gt
gt_done:
    ret
