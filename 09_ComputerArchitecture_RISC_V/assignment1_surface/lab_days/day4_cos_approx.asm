# ============================================================
# DAY 4 — cos_approx only (Exercise A.4)
# Test: cos(0)~1, cos(pi/2)~0, cos(-pi/2)~0
# ============================================================
.data
msg0: .asciz "cos(0) should ~ 1 : "
msgh: .asciz "cos(+pi/2) should ~ 0 : "
msgn: .asciz "cos(-pi/2) should ~ 0 : "
endl: .asciz "\n"
pi:   .double 3.141592653589793
one:  .double 1.0
two:  .double 2.0
twenty4: .double 24.0
seven20: .double 720.0
stack: .space 200

.text
.globl main
main:
    la   t0, stack
    addi sp, t0, 200

    la   a0, msg0
    li   a7, 4
    ecall
    li   t0, 0
    fcvt.d.w fa0, t0
    jal  ra, cos_approx
    li   a7, 3
    ecall
    la   a0, endl
    li   a7, 4
    ecall

    la   a0, msgh
    li   a7, 4
    ecall
    la   t0, pi
    fld  ft0, 0(t0)
    la   t0, two
    fld  ft1, 0(t0)
    fdiv.d fa0, ft0, ft1
    jal  ra, cos_approx
    li   a7, 3
    ecall
    la   a0, endl
    li   a7, 4
    ecall

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
    fsub.d fa0, ft3, ft2
    jal  ra, cos_approx
    li   a7, 3
    ecall
    la   a0, endl
    li   a7, 4
    ecall

    li   a7, 10
    ecall

# cos = 1 - x2/2 + x4/24 - x6/720
cos_approx:
    fmul.d ft0, fa0, fa0       # x2
    fmul.d ft1, ft0, ft0       # x4
    fmul.d ft2, ft1, ft0       # x6
    la   t0, one
    fld  ft3, 0(t0)
    la   t0, two
    fld  ft4, 0(t0)
    fdiv.d ft4, ft0, ft4       # x2/2
    la   t0, twenty4
    fld  ft5, 0(t0)
    fdiv.d ft5, ft1, ft5       # x4/24
    la   t0, seven20
    fld  ft6, 0(t0)
    fdiv.d ft6, ft2, ft6       # x6/720
    fsub.d fa0, ft3, ft4
    fadd.d fa0, fa0, ft5
    fsub.d fa0, fa0, ft6
    ret
