import logging
from Helper_lib import read_file_to_list,Instruction,rotate_right, shift_helper, ByteAddressableMemory,reverse_hex_string_endiannes
from Helper_Student import Log_Datapath,Log_Controller

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
        self.logger = logging.getLogger("Performance Model")
        self.logger.setLevel(logging.DEBUG)
        #Initial values are all 0 as in a FPGA
        self.PC = 0
        self.Register_File =[]
        for i in range(32):
            self.Register_File.append(0)
        #Memory is a special class helper lib to simulate HDL counterpart    
        self.memory = ByteAddressableMemory(1024)
        self.clock_cycle_count = 0    
    #Compares and lgos the PC and register file of Python module and HDL design
    def compare_result(self):
        print("************* Performance Model  **************")
        for i in range(32):
            ref_val = to_signed32(self.Register_File[i])
            print("Register%d: %d \t", i, hex(ref_val))
        

    #A model of the verilog code to confirm operation, data is In_data
    def performance_model (self):
        self.logger.debug("**************** Clock cycle: %d **********************",self.clock_cycle_count)
        self.clock_cycle_count = self.clock_cycle_count + 1
        #Read current instructions, extract and log the fields
        self.logger.debug("**************** Instruction No: %d **********************",int((self.PC)/4))
        current_instruction = self.Instruction_list[int((self.PC)/4)]
        current_instruction = current_instruction.replace(" ", "")
        #We need to reverse the order of bytes since little endian makes the string reversed in Python
        current_instruction = reverse_hex_string_endiannes(current_instruction)
        self.PC = self.PC + 4
        #Flag to check if the current instruction will be executed.
        execute_flag = True
        #Call Instruction calls to get each field from the instruction
        inst_fields = Instruction(current_instruction)
        inst_fields.log(self.logger)
        print(50*"-")
        print("PC: %d", self.PC - 4)
        print("Instruction: %s", current_instruction)
        print("opcode: %s", inst_fields.op)
        print("funct3: %s", inst_fields.funct3)
        print("funct7: %s", inst_fields.funct7)
        print("rd: %d", inst_fields.rd)
        print("rs1: %d", inst_fields.rs1)
        print("rs2: %d", inst_fields.rs2)
        print("imm: %d", inst_fields.imm)
        
        
        if inst_fields.rd < 0 or inst_fields.rd >= len(self.Register_File):
            raise ValueError("Invalid register index")
        
        if(execute_flag):
            if (inst_fields.op == "0110011"):
                R1 = self.Register_File[inst_fields.rs1]
                R2 = self.Register_File[inst_fields.rs2]
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
                    self.logger.debug("Unknown funct7 (%s) value for op (%s)", inst_fields.funct7, inst_fields.op)

            elif (inst_fields.op == "0010011"):
                R1 = self.Register_File[inst_fields.rs1]
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
                R1 = self.Register_File[inst_fields.rs1]
                Imm = inst_fields.imm
                match inst_fields.funct3:
                    case "000": # LB
                        offset = R1 + Imm
                        result = self.memory.read_byte(offset)
                        result = int.from_bytes(result, byteorder='little')
                        result = sign_extend(result, 8)
                        self.Register_File[inst_fields.rd] = result
                    case "001": # LH
                        offset = R1 + Imm
                        result = self.memory.read_halfword(offset)
                        result = int.from_bytes(result, byteorder='little')
                        result = sign_extend(result, 16)
                        self.Register_File[inst_fields.rd] = result
                    case "010": # LW
                        offset = R1 + Imm
                        result = self.memory.read_word(offset)
                        result = int.from_bytes(result, byteorder='little')
                        self.Register_File[inst_fields.rd] = result
                    case "100": # LBU
                        offset = R1 + Imm
                        result = self.memory.read_byte(offset)
                        result = int.from_bytes(result, byteorder='little')
                        self.Register_File[inst_fields.rd] = result 
                    case "101": # LHU
                        offset = R1 + Imm
                        result = self.memory.read_halfword(offset)
                        result = int.from_bytes(result, byteorder='little')
                        self.Register_File[inst_fields.rd] = result
                    
            elif (inst_fields.op == "0100011"):
                R1 = self.Register_File[inst_fields.rs1]
                R2 = self.Register_File[inst_fields.rs2]
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
                R1 = self.Register_File[inst_fields.rs1]
                R2 = self.Register_File[inst_fields.rs2]
                Imm = inst_fields.imm
                R1_Signed = to_signed32(R1)
                R2_Signed = to_signed32(R2)
                match inst_fields.funct3:
                    case "000": # BEQ
                        if (R1_Signed == R2_Signed):
                            self.PC = self.PC + Imm
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
                R1 = self.Register_File[inst_fields.rs1]
                Imm = inst_fields.imm
                result = R1 + Imm
                self.Register_File[inst_fields.rd] = self.PC
                self.PC = (result & 0xFFFFFFFE)
            else:
                self.logger.debug("Unknown opcode: %s", inst_fields.op)

    def run_test(self):
        self.performance_model()
        #Wait 1 us the very first time bc. initially all signals are "X"
        self.compare_result()
        while(int(self.Instruction_list[int((self.PC)/4)].replace(" ", ""),16)!=0):
            self.performance_model()
            #Log datapath and controller before clock edge, this calls user filled functions
            self.compare_result()
            

if __name__ == "__main__":
    #Read the instruction file
    Instruction_list = read_file_to_list("Testbench/Instructions.hex")
    #Create the testbench object
    tb = TB(Instruction_list)
    #Run the test
    tb.run_test()