# Exercise 1.5
# Recursive Fibonacci rewrite of exercise 1.
# fibo(val, cont): if cont!=0 print fib(val) when printing sequence up to N.
# Here: user enters N; we print all Fibonacci numbers F with 0 <= F <= N
# using recursive fibo(k) and a recursive print driver.

.data
prompt:  .asciz "Enter an integer N: "
head:    .asciz "Fibonacci numbers between 0 and N (recursive):\n"
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
    mv   s0, a0             # N

    la   a0, head
    li   a7, 4
    ecall

    # Call fibo_print(index=0) which prints fib(i) while fib(i) <= N
    li   a0, 0              # val = index into sequence
    li   a1, 1              # cont = 1 => print
    jal  ra, fibo
    # fibo with cont=1 prints fib(val) if <= N and recurses to next index

    la   a0, newline
    li   a7, 4
    ecall
    li   a7, 10
    ecall

# ------------------------------------------------------------
# fibo(int val, int cont)
#   a0 = val (Fibonacci index)
#   a1 = cont (if !=0, print fib(val) when fib(val)<=N, then recurse)
# Uses global N in s0. Returns fib(val) in a0 when cont==0.
# When cont!=0: computes F=fib(val); if F>N stop; else print F and fibo(val+1,1)
# ------------------------------------------------------------
fibo:
    addi sp, sp, -32
    sw   ra, 28(sp)
    sw   s1, 24(sp)
    sw   s2, 20(sp)
    sw   s3, 16(sp)

    mv   s1, a0             # index
    mv   s2, a1             # cont

    # Compute fib(index) into s3 using helper fib_n (cont=0 style)
    mv   a0, s1
    jal  ra, fib_n
    mv   s3, a0             # F

    beq  s2, x0, ret_val    # if cont==0 just return F

    # cont != 0: print mode for exercise
    blt  s0, s3, done_rec   # if F > N, stop

    # print F
    mv   a0, s3
    li   a7, 1
    ecall
    la   a0, space
    li   a7, 4
    ecall

    # recurse fibo(index+1, 1)
    addi a0, s1, 1
    li   a1, 1
    jal  ra, fibo
    j    done_rec

ret_val:
    mv   a0, s3

done_rec:
    lw   ra, 28(sp)
    lw   s1, 24(sp)
    lw   s2, 20(sp)
    lw   s3, 16(sp)
    addi sp, sp, 32
    ret

# fib_n(n): classic recursive Fibonacci, returns F_n in a0
# F_0=0, F_1=1
fib_n:
    addi sp, sp, -16
    sw   ra, 12(sp)
    sw   s1, 8(sp)

    mv   s1, a0
    beq  s1, x0, fib0
    li   t0, 1
    beq  s1, t0, fib1

    addi a0, s1, -1
    jal  ra, fib_n
    mv   t1, a0
    sw   t1, 4(sp)

    addi a0, s1, -2
    jal  ra, fib_n
    lw   t1, 4(sp)
    add  a0, a0, t1
    j    fib_done

fib0:
    li   a0, 0
    j    fib_done
fib1:
    li   a0, 1

fib_done:
    lw   ra, 12(sp)
    lw   s1, 8(sp)
    addi sp, sp, 16
    ret
