def read_file_to_list(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()
        lines = [line.strip() for line in lines]
    return lines

class Instruction_Type:
    LUI_INSTR       = "0110111"
    AUIPC_INSTR     = "0010111"
    JAL_INSTR       = "1101111"
    BRANCH_INSTR    = "1100011"
    JALR_INSTR      = "1100111"
    MEM_LOAD_INSTR  = "0000011"
    REG_IMM_INSTR   = "0010011"
    MEM_STORE_INSTR = "0100011"
    CNST_SHFT_INSTR = "0010011"
    REG_REG_INSTR   = "0110011"

class Instruction:
    def __init__(self, instruction):
        self.binary_instr = format(int(instruction, 16), '032b')
        
        self.op = self.binary_instr[(31-6):(32-0)]
        self.rd = int(self.binary_instr[(31-11):(32-7)], 2)
        self.rs1 = int(self.binary_instr[(31-19):(32-15)], 2)
        self.rs2 = int(self.binary_instr[(31-24):(32-20)], 2)
        self.funct3 = int(self.binary_instr[(31-14):(32-12)], 2)
        self.funct7 = int(self.binary_instr[(31-31):(32-25)], 2)
        self.imm = 0
        
    def log(self,logger):
        logger.debug("****** Current Instruction *********")
        logger.debug("Binary string:%s", self.binary_instr)
        logger.debug("op:%s", self.op)
        logger.debug("rd:%d", self.rd)
        logger.debug("rs1:%d", self.rs1)
        logger.debug("rs2:%d", self.rs2)
        logger.debug("funct3:%d", self.funct3)
        logger.debug("funct7:%d", self.funct7)
        logger.debug("imm: %d", self.imm)
        logger.debug("*************************************")
        

def rotate_right(value, shift, n_bits=32):
    shift %= n_bits  # Ensure the shift is within the range of 0 to n_bits-1
    return (value >> shift) | (value << (n_bits - shift)) & ((1 << n_bits) - 1)

def shift_helper(value, shift, shift_type, n_bits=32):
    shift %= n_bits  # Ensure the shift is within the range of 0 to n_bits-1
    match shift_type:
        case 0:
            return (value  << shift)% 0x100000000
        case 1:
            return (value  >> shift) % 0x100000000
        case 2:
            if((value & 0x80000000)!=0):
                    filler = (0xFFFFFFFF >> (n_bits-shift))<<((n_bits-shift))
                    return ((value  >> shift)|filler) % 0x100000000
            else:
                return (value  >> shift) % 0x100000000
        case 3:
            return rotate_right(value,shift,n_bits)
        
def reverse_hex_string_endiannes(hex_string):  
    reversed_string = bytes.fromhex(hex_string)
    reversed_string = reversed_string[::-1]
    reversed_string = reversed_string.hex()        
    return reversed_string

class ByteAddressableMemory:
    def __init__(self, size):
        self.size = size
        self.memory = bytearray(size)  # Initialize memory as a bytearray of the given size

    def read(self, address):
        if address < 0 or address + 4 > self.size:
            raise ValueError("Invalid memory address or length")
        return_val = bytes(self.memory[address : address + 4])
        return_val = return_val[::-1]
        return return_val

    def write(self, address, data):
        if address < 0 or address + 4> self.size:
            raise ValueError("Invalid memory address or data length")
        data_bytes = data.to_bytes(4, byteorder='little')
        self.memory[address : address + 4] = data_bytes        
