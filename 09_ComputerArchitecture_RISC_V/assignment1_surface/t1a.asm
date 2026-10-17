# ============================================================
# Assignment 1 (part 1) — Mathematical surface z = sin(x)*cos(y)
# File based on professor skeleton t1a.asm
# Architecture: RISC-V32 + double FP  |  Simulator: RARS
#
# GROUP MEMBERS (TODO — apna naam likho submission se pehle):
#   Name: _______________  Student ID: _______________
#   Contribution: putpixel / init / sin / cos / surface / testing
#
# HOW TO RUN IN RARS:
#   1) Open this file
#   2) Tools -> Bitmap Display
#        Unit Width/Height = 4 (or 1)
#        Display Width/Height = 512 (for 128x128) or 256 (for 64x64)
#        Base address = address of label "display"
#          (Assemble ke baad Labels window mein "display" dekho)
#          aksar ~ 0x10010000 hota hai — Labels se exact copy karo
#   3) Connect to Program
#   4) Assemble -> Go
# ============================================================

.data
display: .space 65536
colors:
    .word 0x000000  # Black          index 0
    .word 0xFF0000  # Red            index 1
    .word 0x00FF00  # Green
    .word 0x0000FF  # Blue
    .word 0xFFFF00  # Yellow
    .word 0xFF00FF  # Magenta
    .word 0x00FFFF  # Cyan
    .word 0x800000  # Maroon
    .word 0x008000  # Dark Green
    .word 0x000080  # Navy
    .word 0x808000  # Olive
    .word 0x800080  # Purple
    .word 0x008080  # Teal
    .word 0xC0C0C0  # Silver
    .word 0x808080  # Gray
    .word 0xFFA500  # Orange
    .word 0xA52A2A  # Brown
    .word 0xF0E68C  # Khaki
    .word 0xD2691E  # Chocolate
    .word 0xB22222  # Firebrick
    .word 0xFF69B4  # Hot Pink
    .word 0x7FFF00  # Chartreuse
    .word 0x00FF7F  # Spring Green
    .word 0x4682B4  # Steel Blue
    .word 0x5F9EA0  # Cadet Blue
    .word 0xDC143C  # Crimson
    .word 0x8B008B  # Dark Magenta
    .word 0x556B2F  # Dark Olive Green
    .word 0xFF1493  # Deep Pink
    .word 0x1E90FF  # Dodger Blue
    .word 0x32CD32  # Lime Green
    .word 0xFF4500  # Orange Red
    .word 0xDA70D6  # Orchid
    .word 0xEEE8AA  # Pale Goldenrod
    .word 0x98FB98  # Pale Green
    .word 0xAFEEEE  # Pale Turquoise
    .word 0xDB7093  # Pale Violet Red
    .word 0xFFEFD5  # Papaya Whip
    .word 0xFFDAB9  # Peach Puff
    .word 0xCD853F  # Peru
    .word 0xFFC0CB  # Pink
    .word 0xDDA0DD  # Plum
    .word 0xB0E0E6  # Powder Blue
    .word 0x800000  # Repeat Maroon to reach 50 colors
    .word 0x9ACD32
    .word 0x6A5ACD
    .word 0xFF6347
    .word 0x40E0D0
    .word 0xF5DEB3
    .word 0xFFFFFF  # White          index 49  (50 colors total)

stack:.space 100
# Proper domain values (PDF Alg 5). init() bhi yehi ±pi/2 likhta hai.
Maxx: .double 1.5707963267948966   # +pi/2
Maxy: .double 1.5707963267948966   # +pi/2
Minx: .double -1.5707963267948966  # -pi/2
Miny: .double -1.5707963267948966  # -pi/2
conx: .double -0.74
cony: .double 0.1
maxiter: .word 50
resx: .word 128
resy: .word 128
displaybase: .word 0x10000000

pixcorx: .double 0
pixcory: .double 0
str: .asciz " "

# ---- constants for init / sin / cos (hamari additions) ----
pi:          .double 3.141592653589793
one:         .double 1.0
two:         .double 2.0
six:         .double 6.0
twenty4:     .double 24.0
one20:       .double 120.0
seven20:     .double 720.0
five040:     .double 5040.0
numcolsm1:   .double 49.0        # (50 colors - 1)
ncolors:     .word 50

.text
main:
	la sp,stack
	li s1,0
	lw s2 resx
	jal init
looprow:
	li s0,0
loopcol: 
	mv a0,s1
	mv a1,s0
	jal juliapixval
	
	
	mv a2,a0
	mv a0,s1
	mv a1,s0
	
			
	jal putpixel
	
	addi s0,s0,1
	blt s0,s2 loopcol
			
	addi s1,s1,1
	
	blt s1,s2,looprow
	
	li a7,10
	ecall
	
# ============================================================
# init — Algorithm 5
# Pixel-independent setup: domain [-pi/2, pi/2], pixcorx/pixcory
# ============================================================
init:
	# stack pointer fix: skeleton ne sp = stack START diya;
	# stack neeche grow karti hai, isliye END pe le jao
	la   t0, stack
	addi sp, t0, 100

	# save ra (agar baad mein call karein — safe)
	addi sp, sp, -16
	sw   ra, 12(sp)

	# ---- pi load ----
	la   t0, pi
	fld  ft0, 0(t0)              # ft0 = pi

	# half_pi = pi / 2
	la   t0, two
	fld  ft1, 0(t0)              # ft1 = 2.0
	fdiv.d ft2, ft0, ft1         # ft2 = pi/2

	# Maxx = +pi/2 , Minx = -pi/2
	# ft3 = -pi/2  (0 - pi/2), fneg har RARS pe nahi hota
	li   t1, 0
	fcvt.d.w ft3, t1             # 0.0
	fsub.d ft3, ft3, ft2         # 0 - pi/2 = -pi/2
	la   t0, Maxx
	fsd  ft2, 0(t0)
	la   t0, Minx
	fsd  ft3, 0(t0)

	# Maxy = +pi/2 , Miny = -pi/2
	la   t0, Maxy
	fsd  ft2, 0(t0)
	la   t0, Miny
	fsd  ft3, 0(t0)

	# pixcorx = (Maxx - Minx) / cols
	# Maxx-Minx = pi/2 - (-pi/2) = pi
	lw   t1, resx                # t1 = cols (integer)
	fcvt.d.w ft4, t1             # ft4 = cols as double
	fsub.d ft5, ft2, ft3         # ft5 = Maxx - Minx = pi
	fdiv.d ft5, ft5, ft4         # ft5 = pixcorx
	la   t0, pixcorx
	fsd  ft5, 0(t0)

	# pixcory = (Maxy - Miny) / rows
	lw   t1, resy
	fcvt.d.w ft4, t1
	fsub.d ft5, ft2, ft3         # Maxy - Miny = pi
	fdiv.d ft5, ft5, ft4
	la   t0, pixcory
	fsd  ft5, 0(t0)

	# displaybase = real address of "display" (Bitmap ke liye Labels dekho)
	la   t0, display
	la   t1, displaybase
	sw   t0, 0(t1)

	lw   ra, 12(sp)
	addi sp, sp, 16
	ret

# ============================================================
# juliapixval — skeleton name; body = Algorithm 3 surfacepixval
# IN:  a0 = row (ypt), a1 = col (xpt)
# OUT: a0 = colorIndex (integer 0..49)
# ============================================================
juliapixval:
	addi sp, sp, -48
	sw   ra, 44(sp)
	sw   s0, 40(sp)
	sw   s1, 36(sp)
	# save FP callee if needed — we use ft* mostly

	mv   s0, a0                  # s0 = row = ypt
	mv   s1, a1                  # s1 = col = xpt

	# x = col * pixcorx + Minx
	fcvt.d.w ft0, s1             # ft0 = col
	la   t0, pixcorx
	fld  ft1, 0(t0)              # ft1 = pixcorx
	fmul.d ft0, ft0, ft1         # col * pixcorx
	la   t0, Minx
	fld  ft1, 0(t0)
	fadd.d ft0, ft0, ft1         # ft0 = x   (save in fs0 area via memory)
	# keep x in ft8
	fmv.d ft8, ft0

	# y = Maxy - row * pixcory
	fcvt.d.w ft0, s0             # row
	la   t0, pixcory
	fld  ft1, 0(t0)
	fmul.d ft0, ft0, ft1         # row * pixcory
	la   t0, Maxy
	fld  ft1, 0(t0)
	fsub.d ft9, ft1, ft0         # ft9 = y

	# sinx = sin_approx(x)
	fmv.d fa0, ft8
	jal  ra, sin_approx
	fmv.d ft10, fa0              # ft10 = sinx

	# cosy = cos_approx(y)
	fmv.d fa0, ft9
	jal  ra, cos_approx
	fmv.d ft11, fa0              # ft11 = cosy

	# z = sinx * cosy
	fmul.d ft0, ft10, ft11       # ft0 = z

	# color = (z + 1) / 2
	la   t0, one
	fld  ft1, 0(t0)
	fadd.d ft0, ft0, ft1         # z+1
	la   t0, two
	fld  ft1, 0(t0)
	fdiv.d ft0, ft0, ft1         # color in [0,1]

	# colorIndex = color * (numColors - 1)
	la   t0, numcolsm1
	fld  ft1, 0(t0)
	fmul.d ft0, ft0, ft1
	fcvt.w.d t0, ft0             # double -> int color index

	# clamp 0 .. 49 (safety)
	blt  t0, x0, clamp0
	li   t1, 49
	blt  t1, t0, clamp49         # if 49 < t0 then clamp
	j    idx_ok
clamp0:
	li   t0, 0
	j    idx_ok
clamp49:
	li   t0, 49
idx_ok:
	mv   a0, t0

	lw   ra, 44(sp)
	lw   s0, 40(sp)
	lw   s1, 36(sp)
	addi sp, sp, 48
	ret

# ============================================================
# sin_approx — Algorithm 1
# IN:  fa0 = x
# OUT: fa0 = sin(x) approx
# sin = x - x3/6 + x5/120 - x7/5040
# ============================================================
sin_approx:
	# x2 = x*x
	fmul.d ft0, fa0, fa0         # x2
	# x3 = x2*x
	fmul.d ft1, ft0, fa0         # x3
	# x5 = x3*x2
	fmul.d ft2, ft1, ft0         # x5
	# x7 = x5*x2
	fmul.d ft3, ft2, ft0         # x7

	# term1 = x
	fmv.d  ft4, fa0

	# term2 = x3/6
	la   t0, six
	fld  ft5, 0(t0)
	fdiv.d ft5, ft1, ft5

	# term3 = x5/120
	la   t0, one20
	fld  ft6, 0(t0)
	fdiv.d ft6, ft2, ft6

	# term4 = x7/5040
	la   t0, five040
	fld  ft7, 0(t0)
	fdiv.d ft7, ft3, ft7

	# sin = term1 - term2 + term3 - term4
	fsub.d fa0, ft4, ft5
	fadd.d fa0, fa0, ft6
	fsub.d fa0, fa0, ft7
	ret

# ============================================================
# cos_approx — Algorithm 2
# IN:  fa0 = x
# OUT: fa0 = cos(x) approx
# cos = 1 - x2/2 + x4/24 - x6/720
# ============================================================
cos_approx:
	# x2 = x*x
	fmul.d ft0, fa0, fa0
	# x4 = x2*x2
	fmul.d ft1, ft0, ft0
	# x6 = x4*x2
	fmul.d ft2, ft1, ft0

	# term1 = 1
	la   t0, one
	fld  ft3, 0(t0)

	# term2 = x2/2
	la   t0, two
	fld  ft4, 0(t0)
	fdiv.d ft4, ft0, ft4

	# term3 = x4/24
	la   t0, twenty4
	fld  ft5, 0(t0)
	fdiv.d ft5, ft1, ft5

	# term4 = x6/720
	la   t0, seven20
	fld  ft6, 0(t0)
	fdiv.d ft6, ft2, ft6

	# cos = 1 - x2/2 + x4/24 - x6/720
	fsub.d fa0, ft3, ft4
	fadd.d fa0, fa0, ft5
	fsub.d fa0, fa0, ft6
	ret

# ============================================================
# putpixel — Exercise A.1
# IN: a0 = row, a1 = col, a2 = colorIndex
# Writes RGB word from colors[index] into display[row][col]
# ============================================================
putpixel:
	# address = display + 4 * (row * resx + col)
	lw   t0, resx                # cols
	mul  t1, a0, t0              # row * cols
	add  t1, t1, a1              # + col
	slli t1, t1, 2               # * 4 (bytes per pixel)

	la   t0, display             # base of bitmap buffer
	add  t0, t0, t1              # pixel address

	# color word = colors[colorIndex]
	la   t2, colors
	slli t3, a2, 2               # index * 4
	add  t2, t2, t3
	lw   t2, 0(t2)               # RGB

	sw   t2, 0(t0)               # store to bitmap
	ret
