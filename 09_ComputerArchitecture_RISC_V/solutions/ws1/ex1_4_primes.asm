# Exercise 1.4
# Print all prime numbers less than a value given by the user.

.data
prompt:  .asciz "Enter an integer N: "
head:    .asciz "Primes less than N:\n"
space:   .asciz " "
newline: .asciz "\n"

.text
.globl main
main:
    la   a0, prompt
    li   a7, 4
    ecall

    li   a7, 5
    ecall
    mv   s0, a0             # s0 = N

    la   a0, head
    li   a7, 4
    ecall

    li   s1, 2              # candidate = 2
outer:
    bge  s1, s0, done       # while candidate < N

    # is_prime(s1)?
    li   t0, 2              # d = 2
check:
    mul  t1, t0, t0         # d*d
    blt  s1, t1, is_prime   # if d*d > n, prime
    rem  t2, s1, t0         # n % d
    beq  t2, x0, not_prime
    addi t0, t0, 1
    j    check

is_prime:
    mv   a0, s1
    li   a7, 1
    ecall
    la   a0, space
    li   a7, 4
    ecall

not_prime:
    addi s1, s1, 1
    j    outer

done:
    la   a0, newline
    li   a7, 4
    ecall
    li   a7, 10
    ecall
