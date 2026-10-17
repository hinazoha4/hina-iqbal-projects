# ============================================================
# LESSON 1 — Number padho aur wapas print karo
# Syscalls:
#   a7=4 print string
#   a7=5 read int   -> jawab a0 mein
#   a7=1 print int  -> a0 print hota hai
#   a7=10 exit
# ============================================================

.data
ask:  .asciz "Ek number likho: "
say:  .asciz "Tumne likha: "
endl: .asciz "\n"

.text
.globl main
main:
    # poochho
    la   a0, ask
    li   a7, 4
    ecall

    # number lo -> a0 mein aata hai
    li   a7, 5
    ecall

    # a0 save karo (warna string print pe kho jayega)
    mv   t0, a0          # t0 = user number

    # message
    la   a0, say
    li   a7, 4
    ecall

    # number print
    mv   a0, t0
    li   a7, 1
    ecall

    la   a0, endl
    li   a7, 4
    ecall

    li   a7, 10
    ecall
