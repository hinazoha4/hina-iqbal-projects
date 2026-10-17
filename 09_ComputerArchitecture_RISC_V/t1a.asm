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
	
init: # no args
	#pixcorx = (MAxx-Minx)/cols
	# pixcory = ...
	ret

juliapixval: # a0 row, a1 - col, ret color

	ret
	
putpixel: # receives row, col, colorindex
	

	ret
	
