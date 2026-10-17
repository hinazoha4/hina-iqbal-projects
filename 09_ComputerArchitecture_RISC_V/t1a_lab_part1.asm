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
# ---- new constants (added, base data above unchanged) ----
pi:     .double 3.141592653589793
two:    .double 2.0
nl:     .asciz "\n"
msg1:   .asciz "Minx = "
msg2:   .asciz "Maxx = "
msg3:   .asciz "Miny = "
msg4:   .asciz "Maxy = "
msg5:   .asciz "pixcorx = "
msg6:   .asciz "pixcory = "
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
	
# =========================================================
# init  (Exercise A.2 / Algorithm 5)
# Everything that does NOT depend on a single pixel
# =========================================================
init: # no args
	# ft0 = pi
	la    t0, pi
	fld   ft0, 0(t0)

	# ft1 = pi/2
	la    t0, two
	fld   ft2, 0(t0)          # ft2 = 2.0
	fdiv.d ft1, ft0, ft2      # ft1 = pi/2

	# ft3 = -pi/2   (sign flip)
	fneg.d ft3, ft1

	# Maxx = pi/2 , Minx = -pi/2
	la    t0, Maxx
	fsd   ft1, 0(t0)
	la    t0, Minx
	fsd   ft3, 0(t0)

	# Maxy = pi/2 , Miny = -pi/2
	la    t0, Maxy
	fsd   ft1, 0(t0)
	la    t0, Miny
	fsd   ft3, 0(t0)

	# pixcorx = (Maxx - Minx) / cols
	lw    t1, resx
	fcvt.d.w ft4, t1          # int cols -> double
	fsub.d ft5, ft1, ft3      # Maxx - Minx  (= pi)
	fdiv.d ft5, ft5, ft4
	la    t0, pixcorx
	fsd   ft5, 0(t0)

	# pixcory = (Maxy - Miny) / rows
	lw    t1, resy
	fcvt.d.w ft4, t1
	fsub.d ft5, ft1, ft3      # Maxy - Miny  (= pi)
	fdiv.d ft5, ft5, ft4
	la    t0, pixcory
	fsd   ft5, 0(t0)

	# ---- DEMO ONLY: print values in Run I/O to prove init works ----
	mv   t6, ra               # keep return address (jal below changes ra)
	la t2, msg1
	la t3, Minx
	jal printval
	la t2, msg2
	la t3, Maxx
	jal printval
	la t2, msg3
	la t3, Miny
	jal printval
	la t2, msg4
	la t3, Maxy
	jal printval
	la t2, msg5
	la t3, pixcorx
	jal printval
	la t2, msg6
	la t3, pixcory
	jal printval
	mv   ra, t6               # restore return address
	ret

# helper: print text (t2) and the double stored at address t3
printval:
	mv   a0, t2
	li   a7, 4                # print string
	ecall
	fld  fa0, 0(t3)
	li   a7, 3                # print double (fa0)
	ecall
	la   a0, nl
	li   a7, 4
	ecall
	ret

# =========================================================
# juliapixval  (DEMO STUB for now)
# Full version will compute sin/cos. For the lab demo it
# just returns ONE fixed color index -> whole screen 1 color
# =========================================================
juliapixval: # a0 row, a1 - col, ret color
	li a0, 1                  # 1 = Red  (0 = Black, 2 = Green ...)
	ret

# =========================================================
# putpixel  (Exercise A.1)
# a0 = row, a1 = col, a2 = color index
# address = display + 4*(row*cols + col)
# =========================================================
putpixel: # receives row, col, colorindex
	lw   t0, resx             # cols
	mul  t1, a0, t0           # row * cols
	add  t1, t1, a1           # + col
	slli t1, t1, 2            # * 4 bytes per pixel
	la   t0, display
	add  t0, t0, t1           # t0 = pixel address

	la   t2, colors
	slli t3, a2, 2            # index * 4
	add  t2, t2, t3
	lw   t2, 0(t2)            # t2 = RGB value

	sw   t2, 0(t0)            # draw pixel
	ret
