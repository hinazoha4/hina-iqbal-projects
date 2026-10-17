# ============================================================
# DAY 3 — sin_approx only (Exercise A.3)
# Prof ko dikhao: Taylor sin, library NAHI
# Test prints approx values (syscall print double = 3 in RARS)
# ============================================================
.data
msg0:  .asciz "sin(0) should ~ 0 : "
msgh:  .asciz "sin(+pi/2) should ~ 1 : "
msgn:  .asciz "sin(-pi/2) should ~ -1 : "
endl:  .asciz "\n"
pi:    .double 3.141592653589793
two:   .double 2.0
six:   .double 6.0
one20: .double 120.0
five040: .double 5040.0
stack: .space 200

.text
.globl main
main:
    la   t0, stack
    addi sp, t0, 200

    # --- sin(0) ---
    la   a0, msg0
    li   a7, 4
    ecall
    li   t0, 0
    fcvt.d.w fa0, t0
    jal  ra, sin_approx
    li   a7, 3                 # print double
    ecall
    la   a0, endl
    li   a7, 4
    ecall

    # --- sin(pi/2) ---
    la   a0, msgh
    li   a7, 4
    ecall
    la   t0, pi
    fld  ft0, 0(t0)
    la   t0, two
    fld  ft1, 0(t0)
    fdiv.d fa0, ft0, ft1
    jal  ra, sin_approx
    li   a7, 3
    ecall
    la   a0, endl
    li   a7, 4
    ecall

    # --- sin(-pi/2) ---
    la   a0, msgn
    li   a7, 4
    ecall
    la   t0, pi
    fld  ft0, 0(t0)
    la   t0, two
    fld  ft1, 0(t0)
    fdiv.d ft2, ft0, ft1
    li   t1, 0
    fcvt.d.w ft3, t1
    fsub.d fa0, ft3, ft2       # -pi/2
    jal  ra, sin_approx
    li   a7, 3
    ecall
    la   a0, endl
    li   a7, 4
    ecall

    li   a7, 10
    ecall

# sin = x - x3/6 + x5/120 - x7/5040
sin_approx:
    fmul.d ft0, fa0, fa0       # x2
    fmul.d ft1, ft0, fa0       # x3
    fmul.d ft2, ft1, ft0       # x5
    fmul.d ft3, ft2, ft0       # x7
    fmv.d  ft4, fa0            # x
    la   t0, six
    fld  ft5, 0(t0)
    fdiv.d ft5, ft1, ft5       # x3/6
    la   t0, one20
    fld  ft6, 0(t0)
    fdiv.d ft6, ft2, ft6       # x5/120
    la   t0, five040
    fld  ft7, 0(t0)
    fdiv.d ft7, ft3, ft7       # x7/5040
    fsub.d fa0, ft4, ft5
    fadd.d fa0, fa0, ft6
    fsub.d fa0, fa0, ft7
    ret
