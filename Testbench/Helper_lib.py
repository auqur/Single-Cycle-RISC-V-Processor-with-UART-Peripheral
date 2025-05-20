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
        
        self.I = int(self.binary_instr[6], 2)
        self.cmd = int(self.binary_instr[7:11], 2)
        self.S = int(self.binary_instr[11], 2)
        self.Rn = int(self.binary_instr[12:16], 2)
        self.Rd = int(self.binary_instr[16:20], 2)
        self.rot = int(self.binary_instr[20:24], 2)
        self.imm8 = int(self.binary_instr[24:32], 2)
        self.shamt5 = int(self.binary_instr[20:25], 2)
        self.sh = int(self.binary_instr[25:27], 2)
        self.Rm = int(self.binary_instr[28:32], 2)
        self.Rs = int(self.binary_instr[20:24], 2)
        self.imm12 = int(self.binary_instr[20:32], 2)
        self.L = int(self.binary_instr[11], 2)
        if self.binary_instr[8] == '1':
            # Perform sign extension by flipping all bits and subtracting 1
            inverted_string = ''.join('0' if bit == '1' else '1' for bit in self.binary_instr[8:32])
            self.imm24 = -int(inverted_string, 2) - 1
        else:
            # It's a positive number, convert normally
            self.imm24 = int(self.binary_instr[8:32], 2)
        self.L_branch = int(self.binary_instr[7], 2)
        
    def log(self,logger):
        logger.debug("****** Current Instruction *********")
        logger.debug("Binary string:%s", self.binary_instr)
        if(self.binary_instr[4:28]=="000100101111111111110001"):
            logger.debug("Operation type BX")
            logger.debug("Rm: %d",self.Rm)
        elif(self.Op == 0):
            logger.debug("Operation type Data Processing")
            logger.debug("cond:%s ",'{0:X}'.format(self.Cond))
            logger.debug("Immediate bit:%d ",self.I)
            logger.debug("cmd:%s ",'{0:X}'.format(self.cmd))
            logger.debug("Set bit:%d ",self.S)
            logger.debug("Rn:%d \t Rd:%d ",self.Rn,self.Rd)
            if(self.I==1):
                logger.debug("rot:%d \t imm8:%d ",self.rot,self.imm8)
            else:
                logger.debug("shamt5:%d \t sh:%d \t Rm:%d ",self.shamt5,self.sh,self.Rm)
        elif(self.Op == 1):
            logger.debug("Operation type Memory")
            logger.debug("Load bit:%d ",self.L)
            logger.debug("Rn:%d \t Rn:%d ",self.Rn,self.Rd)
            logger.debug("imm12:%d",self.imm12)
        elif(self.Op==2):
            logger.debug("Operation type Branch (except Bx)")
            logger.debug("Link bit:%d ",self.L_branch)
            logger.debug("imm24:%d",self.imm24)
        


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
