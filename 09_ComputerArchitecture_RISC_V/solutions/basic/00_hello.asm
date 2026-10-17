# ============================================================
# LESSON 0 — Hello (sab se pehla program)
# Kaam: screen pe "Hello" likho, phir band
# Registers:
#   a0 = jo print karna hai (address ya number)
#   a7 = kaunsa kaam (4=string, 10=exit)
# ============================================================

.data
msg: .asciz "Hello from RARS!\n"

.text
.globl main
main:
    # Step 1: string ka address a0 mein daalo
    la   a0, msg

    # Step 2: bolo "print string"
    li   a7, 4
    ecall

    # Step 3: program band
    li   a7, 10
    ecall
