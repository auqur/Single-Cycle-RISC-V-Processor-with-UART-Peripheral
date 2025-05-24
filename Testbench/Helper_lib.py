def read_file_to_list(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()
        lines = [line.strip() for line in lines]
    return lines

def extend_to_32bit(value, original_bits, signed=False):
    if signed:
        sign_bit = 1 << (original_bits - 1)
        return (value & (sign_bit - 1)) - (value & sign_bit)
    else:
        return value & ((1 << original_bits) - 1)

def zero_extend_lsb(value):
    bits = len(value)
    result = value + '0' * (32 - bits)
    result = int(result, 2)
    result = extend_to_32bit(result, 32, signed=True)
    return result

class Instruction:
    def __init__(self, instruction):
        self.binary_instr = format(int(instruction, 16), '032b')
        
        self.op = self.binary_instr[(31-6):(32-0)]
        self.rd = int(self.binary_instr[(31-11):(32-7)], 2)
        self.rs1 = int(self.binary_instr[(31-19):(32-15)], 2)
        self.rs2 = int(self.binary_instr[(31-24):(32-20)], 2)
        self.funct3 = self.binary_instr[(31-14):(32-12)]
        self.funct7 = self.binary_instr[(31-31):(32-25)]

        def _I_Imm():
            imm = self.binary_instr[(31-31):(32-20)]
            imm = extend_to_32bit(int(imm, 2), 12, signed=True)
            return imm
        
        def _S_Imm():
            imm = self.binary_instr[(31-31):(32-25)] + self.binary_instr[(31-11):(32-7)]
            imm = extend_to_32bit(int(imm, 2), 12, signed=True)
            return imm
        
        def _B_Imm():
            imm = self.binary_instr[(31-31)] + self.binary_instr[(31-7)] + self.binary_instr[(31-30):(32-25)] + self.binary_instr[(31-11):(32-8)] + '0'
            imm = extend_to_32bit(int(imm, 2), 13, signed=True)
            return imm

        def _U_Imm():
            imm = self.binary_instr[(31-31):(32-12)]
            imm = zero_extend_lsb(imm)
            return imm
        
        def _J_Imm():
            imm = self.binary_instr[(31-31)] + self.binary_instr[(31-19):(32-12)] + self.binary_instr[(31-20)] + self.binary_instr[(31-30):(32-25)] + + self.binary_instr[(31-24):(32-21)] + '0'
            imm = extend_to_32bit(int(imm, 2), 21, signed=True)
            return imm
    
        if self.op in ['1100111', '0000011', '0010011', '0010011']:
            self.imm = _I_Imm()
        elif self.op in ['0110111','0010111']:
            self.imm = _U_Imm()
        elif self.op in ['1101111']:
            self.imm = _J_Imm()
        elif self.op in ['1100011']:
            self.imm = _B_Imm()
        elif self.op in ['0100011']:
            self.imm = _S_Imm()
        else:
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

    def read_word(self, address):
        if address < 0 or address + 4 > self.size:
            raise ValueError("Invalid memory address or length")
        return_val = bytes(self.memory[address : address + 4])
        return_val = int.from_bytes(return_val, byteorder='little')
        return_val = extend_to_32bit(return_val, 32, signed=True)
        return return_val   

    def read_halfword(self, address, signed=True):
        if address < 0 or address + 2 > self.size:
            raise ValueError("Invalid memory address or length")
        return_val = bytes(self.memory[address : address + 2])
        return_val = int.from_bytes(return_val, byteorder='little')
        return_val = extend_to_32bit(return_val, 16, signed=signed)
        return return_val
    
    def read_byte(self, address, signed=True):
        if address < 0 or address >= self.size:
            raise ValueError("Invalid memory address")
        return_val = bytes(self.memory[address: address + 1])
        return_val = int.from_bytes(return_val, byteorder='little')
        return_val = extend_to_32bit(return_val, 8, signed=signed)
        return return_val
    
    def write_word(self, address, data):
        if address < 0 or address + 4> self.size:
            raise ValueError("Invalid memory address or data length")
        data_bytes = data.to_bytes(4, byteorder='little')
        self.memory[address : address + 4] = data_bytes        

    def write_halfword(self, address, data):
        if address < 0 or address + 2 > self.size:
            raise ValueError("Invalid memory address or data length")
        data_bytes = data.to_bytes(2, byteorder='little')
        self.memory[address : address + 2] = data_bytes
        
    def write_byte(self, address, data):
        if address < 0 or address >= self.size:
            raise ValueError("Invalid memory address or data length")
        data_bytes = data.to_bytes(1, byteorder='little')
        self.memory[address: address + 1] = data_bytes