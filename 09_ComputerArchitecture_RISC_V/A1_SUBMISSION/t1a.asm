# Assignment 1 - part 1
# Name: Hina Iqbal
# Student number: uc2023182290
# Contribution: putpixel, init, sin_approx, cos_approx,
#               surfacepixval (tested in RARS 64x64 and 128x128)
#
# z = sin(x)*cos(y) on Bitmap Display (RARS RISC-V32)

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

# constants needed for Alg 1, 2 and 5 (no math library)
pi:    .double 3.141592653589793
c1:    .double 1.0
c2:    .double 2.0
c6:    .double 6.0
c24:   .double 24.0
c120:  .double 120.0
c720:  .double 720.0
c5040: .double 5040.0
c49:   .double 49.0          # numColors-1 (50 colors in table)

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
	jal surfacepixval
	
	
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
	

# init - Algorithm 5 (Min/Max = +/- pi/2, pixcorx, pixcory)
init: # no args
	# stack grows down: put sp at end of stack buffer
	la   t0, stack
	addi t0, t0, 100
	andi sp, t0, -16

	# pi = 3.1415... already in memory; half = pi/2
	la   t0, pi
	fld  ft0, 0(t0)
	la   t0, c2
	fld  ft2, 0(t0)
	fdiv.d ft0, ft0, ft2     # Max = +pi/2
	li   t1, 0
	fcvt.d.w ft1, t1
	fsub.d ft1, ft1, ft0     # Min = -pi/2

	# Minx, Maxx, Miny, Maxy
	la   t0, Maxx
	fsd  ft0, 0(t0)
	la   t0, Minx
	fsd  ft1, 0(t0)
	la   t0, Maxy
	fsd  ft0, 0(t0)
	la   t0, Miny
	fsd  ft1, 0(t0)

	# pixcorx = (Maxx-Minx)/cols
	fsub.d ft3, ft0, ft1
	lw   t1, resx
	fcvt.d.w ft4, t1
	fdiv.d ft5, ft3, ft4
	la   t0, pixcorx
	fsd  ft5, 0(t0)

	# pixcory = (Maxy-Miny)/rows
	lw   t1, resy
	fcvt.d.w ft4, t1
	fdiv.d ft5, ft3, ft4
	la   t0, pixcory
	fsd  ft5, 0(t0)
	ret


# surfacepixval - Algorithm 3
# a0 = row (ypt), a1 = col (xpt)   [same as skeleton]
# return a0 = colorIndex
surfacepixval: # a0 row, a1 - col, ret color
	addi sp, sp, -16
	sw   ra, 12(sp)
	fsd  fs0, 0(sp)

	# x = xpt * pixcorx + Minx
	fcvt.d.w ft0, a1
	la   t0, pixcorx
	fld  ft1, 0(t0)
	fmul.d ft0, ft0, ft1
	la   t0, Minx
	fld  ft1, 0(t0)
	fadd.d ft0, ft0, ft1

	# y = Maxy - ypt * pixcory
	fcvt.d.w ft2, a0
	la   t0, pixcory
	fld  ft1, 0(t0)
	fmul.d ft2, ft2, ft1
	la   t0, Maxy
	fld  ft1, 0(t0)
	fsub.d fs0, ft1, ft2

	# sinx = sin_approx(x)
	fmv.d fa0, ft0
	jal  sin_approx
	fmv.d ft3, fa0

	# cosy = cos_approx(y)
	fmv.d fa0, fs0
	jal  cos_approx

	# z = sinx * cosy
	fmul.d ft0, ft3, fa0

	# color = (z+1)/2
	la   t0, c1
	fld  ft1, 0(t0)
	fadd.d ft0, ft0, ft1
	la   t0, c2
	fld  ft1, 0(t0)
	fdiv.d ft0, ft0, ft1

	# colorIndex = color * (numColors-1)
	la   t0, c49
	fld  ft1, 0(t0)
	fmul.d ft0, ft0, ft1
	fcvt.w.d a0, ft0

	fld  fs0, 0(sp)
	lw   ra, 12(sp)
	addi sp, sp, 16
	ret


# sin_approx - Algorithm 1
# fa0 = x , return fa0
sin_approx:
	fmul.d ft4, fa0, fa0     # x2
	fmul.d ft5, ft4, fa0     # x3
	fmul.d ft6, ft5, ft4     # x5
	fmul.d ft7, ft6, ft4     # x7

	la   t0, c6
	fld  ft8, 0(t0)
	fdiv.d ft5, ft5, ft8     # /6
	la   t0, c120
	fld  ft8, 0(t0)
	fdiv.d ft6, ft6, ft8     # /120
	la   t0, c5040
	fld  ft8, 0(t0)
	fdiv.d ft7, ft7, ft8     # /5040

	fsub.d fa0, fa0, ft5
	fadd.d fa0, fa0, ft6
	fsub.d fa0, fa0, ft7
	ret


# cos_approx - Algorithm 2
# fa0 = x , return fa0
cos_approx:
	fmul.d ft4, fa0, fa0     # x2
	fmul.d ft5, ft4, ft4     # x4
	fmul.d ft6, ft5, ft4     # x6

	la   t0, c2
	fld  ft8, 0(t0)
	fdiv.d ft4, ft4, ft8     # /2
	la   t0, c24
	fld  ft8, 0(t0)
	fdiv.d ft5, ft5, ft8     # /24
	la   t0, c720
	fld  ft8, 0(t0)
	fdiv.d ft6, ft6, ft8     # /720

	la   t0, c1
	fld  fa0, 0(t0)
	fsub.d fa0, fa0, ft4
	fadd.d fa0, fa0, ft5
	fsub.d fa0, fa0, ft6
	ret


# putpixel - Exercise A.1
# a0=row, a1=col, a2=colorindex
putpixel: # receives row, col, colorindex
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
