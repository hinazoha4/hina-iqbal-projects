# ============================================================
# Assignment 1 (part 1) - Surface z = sin(x) * cos(y)
# Architecture: RISC-V32 (RARS), double-precision floating point
#
# Group members and contributions:
#   Name: ____________________   Student no.: __________
#     Contribution: ________________________________
#   Name: ____________________   Student no.: __________
#     Contribution: ________________________________
#
# How to run:
#   Tools -> Bitmap Display
#     Unit Width/Height = 4
#     Display Width/Height = 512   (128x128)  | 256 for 64x64
#     Base address = 0x10010000 (static data)  (label "display")
#   Connect to Program -> Assemble -> Run
# ============================================================
.data
display: .space 65536
colors:
    .word 0x000000  # Black
    .word 0xFF0000  # Red
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
    .word 0xFFFFFF  #White
    
stack:.space 100
Maxx: .double 1.5
Maxy: .double 1.0
Minx: .double -1.5
Miny: .double -1.0
conx: .double -0.74
cony: .double 0.1
maxiter: .word 50
resx: .word 128
resy: .word 128
displaybase: .word 0x10000000

pixcorx: .double 0
pixcory: .double 0
str: .asciz " "

# ---- constants added for the implementation ----
pi:      .double 3.141592653589793
c1:      .double 1.0
c2:      .double 2.0
c6:      .double 6.0
c24:     .double 24.0
c120:    .double 120.0
c720:    .double 720.0
c5040:   .double 5040.0
ncolors: .word 50            # number of colors in the table
colmax:  .double 0           # (ncolors - 1), computed in init
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
# init - Algorithm 5 (Exercise A.2)
# All calculations that do not depend on a single pixel.
# ============================================================
init: # no args
	# The stack grows downwards, so sp must start at the END
	# of the reserved area (aligned to 16 bytes).
	la   t0, stack
	addi t0, t0, 100
	andi sp, t0, -16

	# ft0 = pi/2 , ft1 = -pi/2
	la   t0, pi
	fld  ft0, 0(t0)          # ft0 = pi
	la   t0, c2
	fld  ft2, 0(t0)          # ft2 = 2.0
	fdiv.d ft0, ft0, ft2     # ft0 = pi/2
	fneg.d ft1, ft0          # ft1 = -pi/2

	# Domain: Minx = Miny = -pi/2 , Maxx = Maxy = pi/2
	la   t0, Maxx
	fsd  ft0, 0(t0)
	la   t0, Minx
	fsd  ft1, 0(t0)
	la   t0, Maxy
	fsd  ft0, 0(t0)
	la   t0, Miny
	fsd  ft1, 0(t0)

	# pixcorx = (Maxx - Minx) / cols
	fsub.d ft3, ft0, ft1     # ft3 = Maxx - Minx
	lw   t1, resx
	fcvt.d.w ft4, t1         # ft4 = cols (as double)
	fdiv.d ft5, ft3, ft4
	la   t0, pixcorx
	fsd  ft5, 0(t0)

	# pixcory = (Maxy - Miny) / rows
	lw   t1, resy
	fcvt.d.w ft4, t1         # ft4 = rows (as double)
	fdiv.d ft5, ft3, ft4
	la   t0, pixcory
	fsd  ft5, 0(t0)

	# colmax = numColors - 1
	lw   t1, ncolors
	addi t1, t1, -1
	fcvt.d.w ft6, t1
	la   t0, colmax
	fsd  ft6, 0(t0)
	ret

# ============================================================
# juliapixval - surfacepixval, Algorithm 3 (Exercise A.5)
# in:  a0 = row (ypt), a1 = col (xpt)
# out: a0 = color index
# ============================================================
juliapixval: # a0 row, a1 - col, ret color
	# save ra and fs0 (we call other functions)
	addi sp, sp, -16
	sw   ra, 12(sp)
	fsd  fs0, 0(sp)

	# x = xpt * pixcorx + Minx
	fcvt.d.w ft0, a1         # ft0 = xpt
	la   t0, pixcorx
	fld  ft1, 0(t0)
	fmul.d ft0, ft0, ft1     # xpt * pixcorx
	la   t0, Minx
	fld  ft1, 0(t0)
	fadd.d ft0, ft0, ft1     # ft0 = x

	# y = Maxy - ypt * pixcory
	fcvt.d.w ft2, a0         # ft2 = ypt
	la   t0, pixcory
	fld  ft1, 0(t0)
	fmul.d ft2, ft2, ft1     # ypt * pixcory
	la   t0, Maxy
	fld  ft1, 0(t0)
	fsub.d fs0, ft1, ft2     # fs0 = y (saved register, survives the call)

	# sinx = sinapprox(x)
	fmv.d fa0, ft0
	jal  sinapprox           # fa0 = sin(x)
	fmv.d ft3, fa0           # ft3 = sinx (cosapprox does not use ft3)

	# cosy = cosapprox(y)
	fmv.d fa0, fs0
	jal  cosapprox           # fa0 = cos(y)

	# z = sinx * cosy
	fmul.d ft0, ft3, fa0     # ft0 = z

	# color = (z + 1) / 2
	la   t0, c1
	fld  ft1, 0(t0)
	fadd.d ft0, ft0, ft1     # z + 1
	la   t0, c2
	fld  ft1, 0(t0)
	fdiv.d ft0, ft0, ft1     # color in [0, 1]

	# colorIndex = color * (numColors - 1)
	la   t0, colmax
	fld  ft1, 0(t0)
	fmul.d ft0, ft0, ft1
	fcvt.w.d a0, ft0         # double -> integer index

	# restore and return
	fld  fs0, 0(sp)
	lw   ra, 12(sp)
	addi sp, sp, 16
	ret

# ============================================================
# sinapprox - Algorithm 1 (Exercise A.3)
# in: fa0 = x   out: fa0 = x - x^3/6 + x^5/120 - x^7/5040
# uses only ft4..ft7
# ============================================================
sinapprox:
	fmul.d ft4, fa0, fa0     # ft4 = x2
	fmul.d ft5, ft4, fa0     # ft5 = x3
	fmul.d ft6, ft5, ft4     # ft6 = x5
	fmul.d ft7, ft6, ft4     # ft7 = x7

	la   t0, c6
	fld  ft8, 0(t0)
	fdiv.d ft5, ft5, ft8     # x3/6
	la   t0, c120
	fld  ft8, 0(t0)
	fdiv.d ft6, ft6, ft8     # x5/120
	la   t0, c5040
	fld  ft8, 0(t0)
	fdiv.d ft7, ft7, ft8     # x7/5040

	fsub.d fa0, fa0, ft5     # x - x3/6
	fadd.d fa0, fa0, ft6     #   + x5/120
	fsub.d fa0, fa0, ft7     #   - x7/5040
	ret

# ============================================================
# cosapprox - Algorithm 2 (Exercise A.4)
# in: fa0 = x   out: fa0 = 1 - x^2/2 + x^4/24 - x^6/720
# uses only ft4..ft8
# ============================================================
cosapprox:
	fmul.d ft4, fa0, fa0     # ft4 = x2
	fmul.d ft5, ft4, ft4     # ft5 = x4
	fmul.d ft6, ft5, ft4     # ft6 = x6

	la   t0, c2
	fld  ft8, 0(t0)
	fdiv.d ft4, ft4, ft8     # x2/2
	la   t0, c24
	fld  ft8, 0(t0)
	fdiv.d ft5, ft5, ft8     # x4/24
	la   t0, c720
	fld  ft8, 0(t0)
	fdiv.d ft6, ft6, ft8     # x6/720

	la   t0, c1
	fld  fa0, 0(t0)          # 1
	fsub.d fa0, fa0, ft4     #   - x2/2
	fadd.d fa0, fa0, ft5     #   + x4/24
	fsub.d fa0, fa0, ft6     #   - x6/720
	ret

# ============================================================
# putpixel - Exercise A.1
# in: a0 = row, a1 = col, a2 = color index
# address = display + 4 * (row * cols + col)
# ============================================================
putpixel: # receives row, col, colorindex
	lw   t0, resx            # cols
	mul  t1, a0, t0          # row * cols
	add  t1, t1, a1          # + col
	slli t1, t1, 2           # * 4 bytes per pixel
	la   t0, display
	add  t0, t0, t1          # pixel address

	la   t2, colors
	slli t3, a2, 2           # index * 4
	add  t2, t2, t3
	lw   t2, 0(t2)           # RGB value

	sw   t2, 0(t0)           # draw the pixel
	ret
