def sign_extend(value, bits):
    """Sign-extend a given value to 32 bits"""
    if value & (1 << (bits - 1)):
        value -= 1 << bits
    return value

def extract_immediate(binary_instr, imm_type):
    assert len(binary_instr) == 32

    if imm_type == 'I_IMM':
        imm = binary_instr[0] * 21 + binary_instr[1:12]  # DATA[31], DATA[30:25], DATA[24:21], DATA[20]
        return sign_extend(int(imm, 2), 32)

    elif imm_type == 'S_IMM':
        imm = binary_instr[0] * 21 + binary_instr[1:8]  # DATA[31], DATA[30:25]
        imm += binary_instr[20:24+1] + binary_instr[25]  # DATA[11:8], DATA[7]
        return sign_extend(int(imm, 2), 32)

    elif imm_type == 'B_IMM':
        imm = binary_instr[0] * 20  # DATA[31]
        imm += binary_instr[24]     # DATA[7]
        imm += binary_instr[1:8]    # DATA[30:25]
        imm += binary_instr[20:24+1]  # DATA[11:8]
        imm += '0'                  # 1'b0
        return sign_extend(int(imm, 2), 32)

    elif imm_type == 'U_IMM':
        imm = binary_instr[0] + binary_instr[1:12] + binary_instr[12:20] + '0'*12
        return sign_extend(int(imm, 2), 32)

    elif imm_type == 'J_IMM':
        imm = binary_instr[0]*12           # DATA[31]
        imm += binary_instr[12:20]         # DATA[19:12]
        imm += binary_instr[11]            # DATA[20]
        imm += binary_instr[1:8]           # DATA[30:25]
        imm += binary_instr[8:12]          # DATA[24:21]
        imm += '0'                         # 1'b0
        return sign_extend(int(imm, 2), 32)

    else:
        raise ValueError("Invalid immediate type")

# Example usage:
hex_instr = '00f50793'  # e.g., I-type instruction
binary_instr = format(int(hex_instr, 16), '032b')
imm_val = extract_immediate(binary_instr, 'I_IMM')
print(f"I-type immediate value: {imm_val}")