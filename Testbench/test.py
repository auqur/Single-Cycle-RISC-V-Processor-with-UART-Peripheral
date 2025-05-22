from Helper_lib import *


instr = "234012ef"
binary_instr = format(int(instr, 16), '032b')
print("Binary: " + binary_instr)
instr_class = Instruction(instr[::])
print("op: " + str(instr_class.op))
print("rd: " + str(instr_class.rd))
print("rs1: " + str(instr_class.rs1))
print("rs2: " + str(instr_class.rs2))
print("funct3: " + str(instr_class.funct3))
print("funct7: " + str(instr_class.funct7))
print("imm: ", str(instr_class.imm))