# Imports
import logging
import cocotb
from Helper_lib import read_file_to_list,Instruction,rotate_right, shift_helper, ByteAddressableMemory,reverse_hex_string_endiannes, extend_to_32bit
from Helper_Student import Log_Datapath,Log_Controller, decode_and_print_instruction
from cocotb.clock import Clock
from cocotb.triggers import FallingEdge, RisingEdge, Edge, Timer
from cocotb.binary import BinaryValue

# Converts unsigned to signed 32-bit
def to_signed32(val):
    val = val & 0xFFFFFFFF
    return val if val < 0x80000000 else val - 0x100000000

# Converts signed to unsigned 32-bit
def signed_to_unsigned_32bit(n):
    return n % (1 << 32)

# Testbench class
class TB:
    def __init__(self, Instruction_list,dut,dut_PC,dut_regfile):
        self.dut = dut
        self.dut_PC = dut_PC
        self.dut_regfile = dut_regfile
        self.Instruction_list = Instruction_list
        self.logger = logging.getLogger("Performance Model")
        self.logger.setLevel(logging.DEBUG)
        self.PC = 0
        self.Zero = 0
        self.Register_File =[]
        for i in range(32):
            self.Register_File.append(0)
        self.memory = ByteAddressableMemory(2048)
        self.clock_cycle_count = 0

    # Logs datapath and controller signals
    def log_dut(self):
        Log_Datapath(self.dut,self.logger)
        Log_Controller(self.dut,self.logger)

    # Compares reference model with DUT
    def compare_result(self):
        self.logger.debug("************* Performance Model / DUT Data  **************")
        self.logger.debug("Current PC:%d \t PC:%d",self.PC,self.dut_PC.value.integer)
        for i in range(32):
            ref_val = to_signed32(self.Register_File[i])
            dut_val = to_signed32(self.dut_regfile.Reg_Out[i].value.integer)
            self.logger.debug("Register%d: %d \t %d", i, ref_val, dut_val)
        assert self.PC == self.dut_PC.value
        for i in range(32):
            assert to_signed32(self.Register_File[i]) == to_signed32(self.dut_regfile.Reg_Out[i].value)

    # Python model of the processor
    def performance_model (self):
        self.logger.debug("**************** Clock cycle: %d **********************",self.clock_cycle_count)
        self.clock_cycle_count = self.clock_cycle_count + 1
        self.logger.debug("**************** Instruction No: %d **********************",int((self.PC)/4))
        current_instruction = self.Instruction_list[int((self.PC)/4)]
        current_instruction = current_instruction.replace(" ", "")
        current_instruction = reverse_hex_string_endiannes(current_instruction)
        self.PC = self.PC + 4
        execute_flag = True
        inst_fields = Instruction(current_instruction)
        self.logger.debug("%s", decode_and_print_instruction(inst_fields))
        inst_fields.log(self.logger)
        
        if inst_fields.rd < 0 or inst_fields.rd >= len(self.Register_File):
            raise ValueError("Invalid register index")

        # R-type instructions
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
                        case "010": # SLT
                            if (R1 < R2):
                                self.Register_File[inst_fields.rd] = 1
                            else:
                                self.Register_File[inst_fields.rd] = 0
                        case "011": # SLTU
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
                            result = shift_helper(signed_to_unsigned_32bit(R1), shamt, 1)
                            self.Register_File[inst_fields.rd] = result
                        case "110": # OR
                            result = R1 | R2
                            self.Register_File[inst_fields.rd] = result
                        case "111": # AND
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

            # I-type ALU instructions
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
                    case "101": # SRLI/SRAI
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

            # Load instructions
            elif (inst_fields.op == "0000011"):
                R1 = extend_to_32bit(self.Register_File[inst_fields.rs1], 32, signed=True)
                R1_U = signed_to_unsigned_32bit(R1)
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
                        if (offset == 0x404):
                            result = 0xFFFFFFFF # Special testbench behavior
                        else:
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

            # Store instructions
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

            # Branch instructions
            elif (inst_fields.op == "1100011"):
                R1 = extend_to_32bit(self.Register_File[inst_fields.rs1], 32, signed=True)
                R2 = extend_to_32bit(self.Register_File[inst_fields.rs2], 32, signed=True)
                R1_U = signed_to_unsigned_32bit(R1)
                R2_U = signed_to_unsigned_32bit(R2)
                self.logger.debug("R1_U: %d, R2_U: %d", R1_U, R2_U)
                Imm = inst_fields.imm
                R1_Signed = to_signed32(R1)
                R2_Signed = to_signed32(R2)
                match inst_fields.funct3:
                    case "000": # BEQ
                        if (R1_Signed == R2_Signed):
                            self.PC = self.PC - 4 + Imm
                    case "001": # BNE
                        if (R1_Signed != R2_Signed):
                            self.PC = self.PC - 4 + Imm
                    case "100": # BLT
                        if (R1_Signed < R2_Signed):
                            self.PC = self.PC - 4 + Imm
                    case "101": # BGE
                        if (R1_Signed >= R2_Signed):
                            self.PC = self.PC - 4 + Imm
                    case "110": # BLTU
                        if (R1_U < R2_U):          
                            self.PC = self.PC - 4 + Imm
                    case "111": # BGEU
                        if (R1_U >= R2_U):
                            self.PC = self.PC - 4 + Imm

            # Upper immediate instructions
            elif (inst_fields.op == "0010111"): # AUIPC
                Imm = inst_fields.imm
                result = self.PC - 4 + Imm
                self.Register_File[inst_fields.rd] = result

            elif (inst_fields.op == "0110111"): # LUI
                Imm = inst_fields.imm
                self.Register_File[inst_fields.rd] = Imm

            # Jump instructions
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

    # Main simulation loop
    async def run_test(self):
        self.performance_model()
        await Timer(1, units="us")
        self.log_dut()
        await RisingEdge(self.dut.clk)
        await FallingEdge(self.dut.clk)
        self.compare_result()
        while(int(self.Instruction_list[int((self.PC)/4)].replace(" ", ""),16)!=0):
            self.performance_model()
            self.log_dut()
            await RisingEdge(self.dut.clk)
            await FallingEdge(self.dut.clk)
            self.compare_result()

# Entry point for cocotb test
@cocotb.test()
async def RISCV_Test(dut):
    await cocotb.start(Clock(dut.clk, 10, 'us').start(start_high=False))
    dut.reset.value=1
    await RisingEdge(dut.clk)
    dut.reset.value=0
    await FallingEdge(dut.clk)
    instruction_lines = read_file_to_list('Instructions.hex')
    tb = TB(instruction_lines,dut, dut.Debug_PC, dut.dp.Register_File)
    await tb.run_test()
