#           RISC-V Assembly             Description                                       Address
main:       lui   x1, 0x12345           # x1 = 0x12345000                                 0x0000
            auipc x2, 0x10002           # x2 = PC + 0x10002000                            0x0004
            addi  x3, x0, -17           # x3 = -17                                        0x0008
            addi  x4, x0, 10            # x4 = 10                                         0x000C
            slli  x5, x4, 6             # x5 = x4 << 6 = 640                              0x0010
            srli  x6, x5, 3             # x6 = x5 >> 3 = 80                               0x0014
            srai  x7, x3, 2             # x7 = x3 >> 2 (arith) = -5                       0x0018
            srai  x8, x5, 5             # x8 = x5 >> 5 (arith) = 20                       0x001C
            andi  x9, x8, 12            # x9 = x8 & 12 = 4                                0x0020
            ori   x10, x6, 26           # x10 = x6 | 26 = 90                              0x0024
            xori  x11, x8, 12           # x11 = x8 ^ 12 = 24                              0x0028
            slti  x12, x7, -255         # x12 = (-5 < -255) = 0                           0x002C
            slti  x13, x3, -5           # x13 = (-17 < -5) = 1                            0x0030
            sltiu x14, x3, 17           # x14 = (0xFFFFFFEF < 17) = 0                     0x0034
            sltiu x15, x3, -33          # x15 = (0xFFFFFFEF < 0xFFFFFFDF) = 0             0x0038
            sltiu x16, x3, -9           # x16 = (0xFFFFFFEF < 0xFFFFFFF7) = 1             0x003C
            sb    x5, 4(x9)             # Store byte x5 at address x9 + 4                 0x0040
            sh    x2, -1(x4)            # Store halfword x2 at address x4 - 1             0x0044
            sb    x8, 1(x4)             # Store byte x8 at address x4 + 1                 0x0048
            lw    x17, -12(x8)          # Load word from address x8 - 12 into x17         0x004C
            sw    x1, 3(x13)            # Store word x1 at address x13 + 3                0x0050
            lw    x18, 3(x16)           # Load word from address x16 + 3 into x18         0x0054
            lb    x19, -2(x4)           # x19 = sign-extended byte at x4 - 2              0x0058
            lh    x20, -17(x11)         # x20 = sign-extended halfword at x11 - 17        0x005C
            lbu   x21, 7(x13)           # x21 = zero-extended byte at x13 + 7             0x0060
            lhu   x22, 7(x12)           # x22 = zero-extended halfword at x12 + 7         0x0064
            add   x23, x1, x2           # x23 = x1 + x2                                   0x0068
            sub   x24, x5, x11          # x24 = x5 - x11                                  0x006C
            sll   x25, x2, x23          # x25 = x2 << (x23 & 0x1F)                        0x0070
            slt   x26, x7, x9           # x26 = (-5 < 4) = 1                              0x0074
            sltu  x27, x7, x9           # x27 = (0xFFFFFFFB < 0x00000004) = 0             0x0078
            sltu  x28, x9, x7           # x28 = (0x00000004 < 0xFFFFFFFB) = 1             0x007C
            xor   x29, x23, x1          # x29 = x23 ^ x1                                  0x0080
            srl   x30, x1, x11          # x30 = x1 >> (x11 & 0x1F)                        0x0084
            sra   x31, x20, x9          # x31 = x20 >> (x9 & 0x1F) (arith)                0x0088
            or    x12, x5, x6           # x12 = x5 | x6                                   0x008C
            and   x14, x10, x24         # x14 = x10 & x24                                 0x0090
            beq   x1, x18, brancheq     # Branch to 'brancheq' if x1 == x18               0x0094
            slti  x1, x0, 1             # x1 = (0 < 1) = 1                                0x0098
brancheq:   beq   x1, x2, infloop       # Branch to 'infloop' if x1 == x2                 0x009C
            bne   x19, x20, branchne    # Branch to 'branchne' if x19 != x20              0x00A0
            slti  x2, x0, 1             # x2 = (0 < 1) = 1                                0x00A4
branchne:   bne   x1, x18, infloop      # Branch to 'infloop' if x1 != x18                0x00A8
            blt   x20, x19, branchlt    # Branch to 'branchlt' if x20 < x19               0x00AC
            slti  x3, x0, 1             # x3 = (0 < 1) = 1                                0x00B0
branchlt:   blt   x9, x7, infloop       # Branch to 'infloop' if x9 < x7                  0x00B4
            bge   x23, x3, branchge     # Branch to 'branchge' if x23 >= x3               0x00B8
            slti  x4, x0, 1             # x4 = (0 < 1) = 1                                0x00BC
branchge:   bge   x20, x7, infloop      # Branch to 'infloop' if x20 >= x7                0x00C0
            bltu  x18, x20, branchltu   # Branch to 'branchltu' if x18 < x20 (unsigned)   0x00C4
            slti  x5, x0, 1             # x5 = (0 < 1) = 1                                0x00C8
branchltu:  bltu  x19, x20, infloop     # Branch to 'infloop' if x19 < x20 (unsigned)     0x00CC
            bgeu  x7, x23, branchgeu    # Branch to 'branchgeu' if x7 >= x23 (unsigned)   0x00D0
            slti  x6, x0, 1             # x6 = (0 < 1) = 1                                0x00D4
branchgeu:  bgeu  x10, x7, infloop      # Branch to 'infloop' if x10 >= x7 (unsigned)     0x00D8
            jalr  x15, x5, -412         # Jump to x5 - 412, x15 = return address          0x00DC
            slti  x7, x0, 1             # x7 = (0 < 1) = 1                                0x00E0
            jal   x16, cont             # Jump to 'cont', x16 = return address            0x00E4
            slti  x8, x0, 1             # x8 = (0 < 1) = 1                                0x00E8
cont:       add   x27, x23, x18         # x27 = x23 + x18                                 0x00EC
nopr:       nop                         # No operation                                    0x00F0
            addi  x1, x1, 1             # x1 = x1 + 1                                     0x00F4
            beq   x0, x0, nopr          # Infinite loop at 'nopr'                         0x00F8
infloop:    beq   x0, x0, infloop       # Infinite loop at 'infloop'                      0x00FC