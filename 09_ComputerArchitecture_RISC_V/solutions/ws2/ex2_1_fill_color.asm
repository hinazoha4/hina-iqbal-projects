# Exercise 2.1
# Fill all Bitmap Display pixels with a solid color.
# Setup in RARS: Tools -> Bitmap Display
#   Display Width/Height: 256 x 256
#   Unit Width/Height: 4 x 4  => 64x64 virtual pixels
#   Base address: 0x10010000
#   Connect to Program (button)
#
# Change COLOR below to try: white, red, green, custom

# Bitmap Display base: set tool to 0x10040000 (avoids clashing with .data)
.eqv DISPLAY_BASE 0x10040000
.eqv NUM_PIXELS   4096          # 64*64

# Colors (0x00RRGGBB)
.eqv COLOR_WHITE  0x00FFFFFF
.eqv COLOR_RED    0x00FF0000
.eqv COLOR_GREEN  0x0000FF00
.eqv COLOR_CUSTOM 0x00328040    # (50,128,64)

.data
# Pick which color to use by changing the word below
fill_color: .word COLOR_WHITE

.text
.globl main
main:
    li   t0, DISPLAY_BASE
    lw   t1, fill_color
    li   t2, NUM_PIXELS

loop:
    beq  t2, x0, done
    sw   t1, 0(t0)
    addi t0, t0, 4
    addi t2, t2, -1
    j    loop

done:
    li   a7, 10
    ecall
