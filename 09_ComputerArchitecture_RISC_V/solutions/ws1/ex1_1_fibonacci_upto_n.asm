# Exercise 1.1
# Prompt user for an integer N, print Fibonacci numbers between 0 and N.
# (Classic sequence starting 0, 1, 1, 2, 3, 5, ... while F <= N)

.data
prompt:  .asciz "Enter an integer N: "
head:    .asciz "Fibonacci numbers between 0 and N:\n"
space:   .asciz " "
newline: .asciz "\n"

.text
.globl main
main:
    la   a0, prompt
    li   a7, 4
    ecall

    li   a7, 5              # read_int -> a0
    ecall
    mv   s0, a0             # s0 = N

    la   a0, head
    li   a7, 4
    ecall

    # Handle N < 0: print nothing
    blt  s0, x0, done

    # Print F0 = 0 if 0 <= N
    li   a0, 0
    li   a7, 1
    ecall
    la   a0, space
    li   a7, 4
    ecall

    # If N == 0, stop after 0
    beq  s0, x0, done

    # Print F1 = 1 if 1 <= N
    li   a0, 1
    li   a7, 1
    ecall
    la   a0, space
    li   a7, 4
    ecall

    li   t0, 0              # prev = F0
    li   t1, 1              # curr = F1

next:
    add  t2, t0, t1         # next = prev + curr
    blt  s0, t2, done       # if next > N, stop
    mv   a0, t2
    li   a7, 1
    ecall
    la   a0, space
    li   a7, 4
    ecall
    mv   t0, t1             # prev = curr
    mv   t1, t2             # curr = next
    j    next

done:
    la   a0, newline
    li   a7, 4
    ecall
    li   a7, 10
    ecall
