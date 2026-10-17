# ============================================================
# EXERCISE 1.8 (BEGINNER) — Digits ke English names
# Example: 352 -> three five two
#
# Plan:
#   1) digits nikal ke array mein daalo (pehle last digit)
#   2) ulta print karo (pehla digit pehle)
#
# Reminder:
#   rem  t, n, 10   => last digit
#   div  n, n, 10   => baaki number
# ============================================================

.data
ask:    .asciz "Positive number likho: "
space:  .asciz " "
endl:   .asciz "\n"
zero:   .asciz "zero"
one:    .asciz "one"
two:    .asciz "two"
three:  .asciz "three"
four:   .asciz "four"
five:   .asciz "five"
six:    .asciz "six"
seven:  .asciz "seven"
eight:  .asciz "eight"
nine:   .asciz "nine"
names:  .word zero, one, two, three, four, five, six, seven, eight, nine
digits: .space 40          # max ~10 digits

.text
.globl main
main:
    la   a0, ask
    li   a7, 4
    ecall
    li   a7, 5
    ecall
    mv   s0, a0            # number

    # special: 0
    bne  s0, x0, extract
    la   a0, zero
    li   a7, 4
    ecall
    j    endline

extract:
    la   s2, digits        # array base
    li   s1, 0             # count = 0
    li   t3, 10

take_digit:
    beq  s0, x0, print_all
    rem  t0, s0, t3        # digit
    div  s0, s0, t3
    slli t1, s1, 2         # count * 4
    add  t1, s2, t1
    sw   t0, 0(t1)         # digits[count] = digit
    addi s1, s1, 1
    j    take_digit

print_all:
    addi s3, s1, -1        # index = count-1
print_one:
    blt  s3, x0, endline
    slli t1, s3, 2
    add  t1, s2, t1
    lw   t0, 0(t1)         # digit value 0..9

    # names[digit] ka address lao
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
    j    print_one

endline:
    la   a0, endl
    li   a7, 4
    ecall
    li   a7, 10
    ecall
