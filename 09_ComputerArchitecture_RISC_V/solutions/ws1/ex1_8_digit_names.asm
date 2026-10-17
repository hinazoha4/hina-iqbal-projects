# Exercise 1.8
# Given a positive integer, print the English names of its digits.
# Example: 352 -> three five two

.data
prompt:  .asciz "Enter a positive integer: "
space:   .asciz " "
newline: .asciz "\n"
zero:    .asciz "zero"
one:     .asciz "one"
two:     .asciz "two"
three:   .asciz "three"
four:    .asciz "four"
five:    .asciz "five"
six:     .asciz "six"
seven:   .asciz "seven"
eight:   .asciz "eight"
nine:    .asciz "nine"

# table of string addresses (will fill at runtime via labels)
names:
    .word zero, one, two, three, four, five, six, seven, eight, nine

# buffer for digits (max 10 digits for 32-bit)
digits: .space 40

.text
.globl main
main:
    la   a0, prompt
    li   a7, 4
    ecall
    li   a7, 5
    ecall
    mv   s0, a0             # number

    # Special case 0
    bne  s0, x0, extract
    la   t0, names
    lw   a0, 0(t0)
    li   a7, 4
    ecall
    la   a0, newline
    li   a7, 4
    ecall
    j    exit

extract:
    # Extract digits into array (least significant first), count in s1
    la   s2, digits
    li   s1, 0
    li   t3, 10

ext_loop:
    beq  s0, x0, print_digits
    rem  t0, s0, t3         # digit = n % 10
    div  s0, s0, t3         # n = n / 10
    slli t1, s1, 2
    add  t1, s2, t1
    sw   t0, 0(t1)
    addi s1, s1, 1
    j    ext_loop

print_digits:
    # Print from most significant (index s1-1 down to 0)
    addi s3, s1, -1

print_loop:
    blt  s3, x0, end_print
    slli t1, s3, 2
    add  t1, s2, t1
    lw   t0, 0(t1)          # digit

    # names[digit]
    la   t2, names
    slli t0, t0, 2
    add  t2, t2, t0
    lw   a0, 0(t2)
    li   a7, 4
    ecall

    la   a0, space
    li   a7, 4
    ecall

    addi s3, s3, -1
    j    print_loop

end_print:
    la   a0, newline
    li   a7, 4
    ecall

exit:
    li   a7, 10
    ecall
