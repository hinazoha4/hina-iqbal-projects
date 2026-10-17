# Ex 2.5 - Easy (simple PGM viewer)
# P5 PGM file padho, Bitmap pe dikhao (max 64x64)
# Baaki screen black
# Bitmap base 0x10040000, Connect!
#
# Test file (agar ho):
#   easy_solutions\ws2\tiny.pgm
# Full path do jab poochhe

.eqv BASE 0x10040000

.data
ask:  .asciz "PGM path: "
bad:  .asciz "Open/magic fail\n"
ok:   .asciz "Done\n"
fname:.space 128
hdr:  .space 256

.text
.globl main
main:
    # black fill
    li   t0, BASE
    li   t1, 4096
bf:
    beq  t1, x0, after
    sw   x0, 0(t0)
    addi t0, t0, 4
    addi t1, t1, -1
    j    bf
after:
    la   a0, ask
    li   a7, 4
    ecall
    la   a0, fname
    li   a1, 128
    li   a7, 8
    ecall
    # strip newline
    la   t0, fname
st:
    lbu  t1, 0(t0)
    beq  t1, x0, stok
    li   t2, 10
    beq  t1, t2, sn
    li   t2, 13
    beq  t1, t2, sn
    addi t0, t0, 1
    j    st
sn: sb   x0, 0(t0)
stok:
    la   a0, fname
    li   a1, 0
    li   a7, 1024
    ecall
    blt  a0, x0, fail
    mv   s0, a0              # fd

    mv   a0, s0
    la   a1, hdr
    li   a2, 256
    li   a7, 63
    ecall
    mv   s1, a0              # bytes
    la   s2, hdr

    # check P5
    lbu  t0, 0(s2)
    li   t1, 80
    bne  t0, t1, fail2
    lbu  t0, 1(s2)
    li   t1, 53
    bne  t0, t1, fail2
    addi s2, s2, 2

    jal  ra, skip
    jal  ra, pint
    mv   s3, a0              # W
    jal  ra, skip
    jal  ra, pint
    mv   s4, a0              # H
    jal  ra, skip
    jal  ra, pint            # maxval (ignore scale)
    addi s2, s2, 1           # skip 1 whitespace

    la   t0, hdr
    sub  s6, s2, t0          # header len
    sub  s7, s1, s6          # leftover bytes

    li   t0, 64
    blt  s3, t0, wok
    li   s3, 64
wok:
    blt  s4, t0, hok
    li   s4, 64
hok:
    li   s8, 0               # row
rloop:
    bge  s8, s4, fin
    li   s9, 0
cloop:
    bge  s9, s3, nr
    ble  s7, x0, refill
have:
    lbu  t0, 0(s2)
    addi s2, s2, 1
    addi s7, s7, -1
    mv   t1, t0
    slli t2, t1, 16
    slli t3, t1, 8
    or   t2, t2, t3
    or   t2, t2, t1
    slli t4, s8, 6
    add  t4, t4, s9
    slli t4, t4, 2
    li   t5, BASE
    add  t4, t4, t5
    sw   t2, 0(t4)
    addi s9, s9, 1
    j    cloop
refill:
    mv   a0, s0
    la   a1, hdr
    li   a2, 256
    li   a7, 63
    ecall
    ble  a0, x0, fin
    mv   s7, a0
    la   s2, hdr
    j    have
nr:
    addi s8, s8, 1
    j    rloop

fin:
    mv   a0, s0
    li   a7, 57
    ecall
    la   a0, ok
    li   a7, 4
    ecall
    li   a7, 10
    ecall

fail:
    la   a0, bad
    li   a7, 4
    ecall
    li   a7, 10
    ecall
fail2:
    la   a0, bad
    li   a7, 4
    ecall
    mv   a0, s0
    li   a7, 57
    ecall
    li   a7, 10
    ecall

skip:
sk:
    lbu  t0, 0(s2)
    li   t1, 32
    beq  t0, t1, adv
    li   t1, 9
    beq  t0, t1, adv
    li   t1, 10
    beq  t0, t1, adv
    li   t1, 13
    beq  t0, t1, adv
    ret
adv:
    addi s2, s2, 1
    j    sk

pint:
    li   a0, 0
pl:
    lbu  t0, 0(s2)
    li   t1, 48
    blt  t0, t1, pd
    li   t1, 57
    blt  t1, t0, pd
    addi t0, t0, -48
    li   t1, 10
    mul  a0, a0, t1
    add  a0, a0, t0
    addi s2, s2, 1
    j    pl
pd: ret
