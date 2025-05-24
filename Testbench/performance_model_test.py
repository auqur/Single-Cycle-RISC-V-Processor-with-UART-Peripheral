# ==============================================================================
# Authors:              Doğu Erkan Arkadaş
#
# Cocotb Testbench:     For Single Cycle ARM Laboratory
#
# Description:
# ------------------------------------
# Test bench for the single cycle laboratory, used by the students to check their designs
#
# License:
# ==============================================================================

from Helper_lib import read_file_to_list,Instruction,rotate_right, shift_helper, ByteAddressableMemory,reverse_hex_string_endiannes, extend_to_32bit
from Helper_Student import decode_and_print_instruction
def to_signed32(val):
    val = val & 0xFFFFFFFF  # Mask to 32 bits
    return val if val < 0x80000000 else val - 0x100000000

def sign_extend(value, bits):
    sign_bit = value[0]
    return sign_bit * (32 - bits) + value

class TB:
    def __init__(self, Instruction_list):

        self.Instruction_list = Instruction_list
        #Configure the logger
        #Initial values are all 0 as in a FPGA
        self.PC = 0
        self.Zero = 0
        self.Register_File =[]
        for i in range(32):
            self.Register_File.append(0)
        #Memory is a special class helper lib to simulate HDL counterpart    
        self.memory = ByteAddressableMemory(2048)
        self.clock_cycle_count = 0        


    #Compares and lgos the PC and register file of Python module and HDL design
    def compare_result(self):       
        for i in range(32):
            ref_val = to_signed32(self.Register_File[i])
            print("Register%d: %d", i, ref_val)


    #A model of the verilog code to confirm operation, data is In_data
    def performance_model (self):
        print("**************** Clock cycle: %d **********************",self.clock_cycle_count)
        self.clock_cycle_count = self.clock_cycle_count + 1
        #Read current instructions, extract and log the fields
        print("**************** Instruction No: %d **********************",int((self.PC)/4))
        current_instruction = self.Instruction_list[int((self.PC)/4)]
        current_instruction = current_instruction.replace(" ", "")
        print("PC: %d", self.PC)
        #We need to reverse the order of bytes since little endian makes the string reversed in Python
        current_instruction = reverse_hex_string_endiannes(current_instruction)
        self.PC = self.PC + 4
        #Flag to check if the current instruction will be executed.
        execute_flag = True
        #Call Instruction calls to get each field from the instruction
        inst_fields = Instruction(current_instruction)
        decode_and_print_instruction(inst_fields)
        print("Instruction: %s", current_instruction)
        print("Opcode: %s", inst_fields.op)
        print("Funct3: %s", inst_fields.funct3)
        print("Funct7: %s", inst_fields.funct7)
        print("rd: %d", inst_fields.rd)
        print("rs1: %d", inst_fields.rs1)
        print("rs2: %d", inst_fields.rs2)
        print("Imm: %d", inst_fields.imm)
        
        
        if inst_fields.rd < 0 or inst_fields.rd >= len(self.Register_File):
            raise ValueError("Invalid register index")

        if(execute_flag):
            if (inst_fields.op == "0110011"):
                R1 = extend_to_32bit(self.Register_File[inst_fields.rs1], 32, signed=True)
                R2 = extend_to_32bit(self.Register_File[inst_fields.rs2], 32, signed=True)
                shamt = R2 & 0x1F
                if (inst_fields.funct7 == "0000000"):
                    match inst_fields.funct3:
                        case "000": # ADD
                            result = R1 + R2
                            self.Register_File[inst_fields.rd] = result
                        case "001": # SLL
                            result = shift_helper(R1, shamt, 0)
                            self.Register_File[inst_fields.rd] = result
                        case "010": #SLT
                            if (R1 < R2):
                                self.Register_File[inst_fields.rd] = 1
                            else:
                                self.Register_File[inst_fields.rd] = 0
                        case "011": #SLTU
                            R1 = R1 & 0xFFFFFFFF
                            R2 = R2 & 0xFFFFFFFF
                            if (R1 < R2):
                                self.Register_File[inst_fields.rd] = 1
                            else:
                                self.Register_File[inst_fields.rd] = 0
                        case "100": # XOR
                            result = R1 ^ R2
                            self.Register_File[inst_fields.rd] = result
                        case "101": # SRL
                            result = shift_helper(R1, shamt, 1)
                            self.Register_File[inst_fields.rd] = result
                        case "110": # OR
                            result = R1 | R2
                            self.Register_File[inst_fields.rd] = result
                        case "111":
                            result = R1 & R2
                            self.Register_File[inst_fields.rd] = result
                
                elif (inst_fields.funct7 == "0100000"):
                    match inst_fields.funct3:
                        case "000": # SUB
                            result = R1 - R2
                            self.Register_File[inst_fields.rd] = result
                        case "101": # SRA
                            result = shift_helper(R1, shamt, 2)
                            self.Register_File[inst_fields.rd] = result
                else:
                    print("Unknown funct7 (%s) value for op (%s)", inst_fields.funct7, inst_fields.op)

            elif (inst_fields.op == "0010011"):
                R1 = extend_to_32bit(self.Register_File[inst_fields.rs1], 32, signed=True)
                Imm = inst_fields.imm
                shamt = inst_fields.rs2
                match inst_fields.funct3:
                    case "000": # ADDI
                        result = R1 + Imm
                        self.Register_File[inst_fields.rd] = result 
                    case "001": # SLLI
                        result = shift_helper(R1, shamt, 0)
                        self.Register_File[inst_fields.rd] = result
                    case "010": # SLTI
                        if (R1 < Imm):
                            self.Register_File[inst_fields.rd] = 1
                        else:
                            self.Register_File[inst_fields.rd] = 0
                    case "011": # SLTIU
                        R1 = R1 & 0xFFFFFFFF
                        Imm = Imm & 0xFFFFFFFF
                        if (R1 < Imm):
                            self.Register_File[inst_fields.rd] = 1
                        else:
                            self.Register_File[inst_fields.rd] = 0
                    case "100": # XORI
                        result = R1 ^ Imm
                        self.Register_File[inst_fields.rd] = result
                    case "101": # SRLI & SRAI
                        if (inst_fields.funct7 == "0000000"):
                            result = shift_helper(R1, shamt, 1)
                        elif (inst_fields.funct7 == "0100000"):
                            result = shift_helper(R1, shamt, 2)
                        self.Register_File[inst_fields.rd] = result
                    case "110": # ORI
                        result = R1 | Imm
                        self.Register_File[inst_fields.rd] = result
                    case "111": # ANDI
                        result = R1 & Imm
                        self.Register_File[inst_fields.rd] = result
    
            elif (inst_fields.op == "0000011"):
                R1 = extend_to_32bit(self.Register_File[inst_fields.rs1], 32, signed=True)
                Imm = inst_fields.imm
                match inst_fields.funct3:
                    case "000": # LB
                        offset = R1 + Imm
                        result = self.memory.read_byte(offset, signed=True)
                        self.Register_File[inst_fields.rd] = result
                    case "001": # LH
                        offset = R1 + Imm
                        result = self.memory.read_halfword(offset, signed=True)
                        self.Register_File[inst_fields.rd] = result
                    case "010": # LW
                        offset = R1 + Imm
                        result = self.memory.read_word(offset)
                        self.Register_File[inst_fields.rd] = result
                    case "100": # LBU
                        offset = R1 + Imm
                        result = self.memory.read_byte(offset, signed=False)
                        self.Register_File[inst_fields.rd] = result 
                    case "101": # LHU
                        offset = R1 + Imm
                        result = self.memory.read_halfword(offset, signed=False)
                        self.Register_File[inst_fields.rd] = result
                    
            elif (inst_fields.op == "0100011"):
                R1 = extend_to_32bit(self.Register_File[inst_fields.rs1], 32, signed=True)
                R2 = extend_to_32bit(self.Register_File[inst_fields.rs2], 32, signed=True)
                Imm = inst_fields.imm
                match inst_fields.funct3:
                    case "000": # SB
                        offset = R1 + Imm
                        data = R2 & 0xFF
                        self.memory.write_byte(offset, data)
                    case "001": # SH    
                        offset = R1 + Imm
                        data = R2 & 0xFFFF
                        self.memory.write_halfword(offset, data)
                    case "010": # SW
                        offset = R1 + Imm
                        data = R2 & 0xFFFFFFFF
                        self.memory.write_word(offset, data)
                        
            elif (inst_fields.op == "1100011"):
                R1 = extend_to_32bit(self.Register_File[inst_fields.rs1], 32, signed=True)
                R2 = extend_to_32bit(self.Register_File[inst_fields.rs2], 32, signed=True)
                Imm = inst_fields.imm
                R1_Signed = to_signed32(R1)
                R2_Signed = to_signed32(R2)
                match inst_fields.funct3:
                    case "000": # BEQ
                        if (R1_Signed == R2_Signed):
                            self.PC = self.PC - 4 + Imm
                    case "001": # BNE
                        if (R1_Signed != R2_Signed):
                            self.PC = self.PC + Imm
                    case "100": # BLT
                        if (R1_Signed < R2_Signed):
                            self.PC = self.PC + Imm
                    case "101": # BGE
                        if (R1_Signed >= R2_Signed):
                            self.PC = self.PC + Imm
                    case "110": # BLTU
                        if (R1 < R2):
                            self.PC = self.PC + Imm
                    case "111":
                        if (R1 >= R2):
                            self.PC = self.PC + Imm

            elif (inst_fields.op == "0010111"): # AUIPC
                Imm = inst_fields.imm
                result = self.PC - 4 + Imm
                self.Register_File[inst_fields.rd] = result
            
            elif (inst_fields.op == "0110111"): # LUI                    
                Imm = inst_fields.imm
                self.Register_File[inst_fields.rd] = Imm
    
            elif (inst_fields.op == "1101111"): # JAL
                Imm = inst_fields.imm
                self.Register_File[inst_fields.rd] = self.PC
                self.PC = self.PC - 4 + Imm
                
            elif (inst_fields.op == "1100111"): # JALR
                R1 = extend_to_32bit(self.Register_File[inst_fields.rs1], 32, signed=True)
                Imm = inst_fields.imm
                result = R1 + Imm
                self.Register_File[inst_fields.rd] = self.PC
                self.PC = (result & 0xFFFFFFFE)
            else:
                print("Unknown opcode: %s", inst_fields.op)

    def run_test(self):
        self.performance_model()
        #Wait 1 us the very first time bc. initially all signals are "X"
        self.compare_result()
        while(int(self.Instruction_list[int((self.PC)/4)].replace(" ", ""),16)!=0):
            self.performance_model()
            self.compare_result()
            
def Single_cycle_test():
    #Generate the clock
    instruction_lines = read_file_to_list('Testbench/Instructions.hex')
    #Give PC signal handle and Register File MODULE handle
    tb = TB(instruction_lines)
    tb.run_test()
    
    
    
if __name__ == "__main__":
    Single_cycle_test()
    print("Test completed successfully.")
    #The testbench will be run by cocotb, so no need to call it here
    #cocotb.start_soon(Single_cycle_test())
