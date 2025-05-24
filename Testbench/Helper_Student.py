def ToHex(value):
    try:
        ret = hex(value.integer)
    except: #If there are 'x's in the value
        ret = "0b" + str(value)
    return ret

def decode_and_print_instruction(inst_fields):
    op = inst_fields.op
    funct3 = inst_fields.funct3
    funct7 = inst_fields.funct7
    rd = f"x{inst_fields.rd}"
    rs1 = f"x{inst_fields.rs1}"
    rs2 = f"x{inst_fields.rs2}"
    imm = inst_fields.imm

    instr_str = "UNKNOWN"

    if op == "0110011":  # R-type
        if funct7 == "0000000":
            match funct3:
                case "000": instr_str = f"ADD  {rd}, {rs1}, {rs2}"
                case "001": instr_str = f"SLL  {rd}, {rs1}, {rs2}"
                case "010": instr_str = f"SLT  {rd}, {rs1}, {rs2}"
                case "011": instr_str = f"SLTU {rd}, {rs1}, {rs2}"
                case "100": instr_str = f"XOR  {rd}, {rs1}, {rs2}"
                case "101": instr_str = f"SRL  {rd}, {rs1}, {rs2}"
                case "110": instr_str = f"OR   {rd}, {rs1}, {rs2}"
                case "111": instr_str = f"AND  {rd}, {rs1}, {rs2}"
        elif funct7 == "0100000":
            match funct3:
                case "000": instr_str = f"SUB  {rd}, {rs1}, {rs2}"
                case "101": instr_str = f"SRA  {rd}, {rs1}, {rs2}"

    elif op == "0010011":  # I-type (ALU immediates)
        match funct3:
            case "000": instr_str = f"ADDI  {rd}, {rs1}, {imm}"
            case "001": instr_str = f"SLLI  {rd}, {rs1}, {inst_fields.rs2}"
            case "010": instr_str = f"SLTI  {rd}, {rs1}, {imm}"
            case "011": instr_str = f"SLTIU {rd}, {rs1}, {imm}"
            case "100": instr_str = f"XORI  {rd}, {rs1}, {imm}"
            case "101":
                if funct7 == "0000000":
                    instr_str = f"SRLI  {rd}, {rs1}, {inst_fields.rs2}"
                elif funct7 == "0100000":
                    instr_str = f"SRAI  {rd}, {rs1}, {inst_fields.rs2}"
            case "110": instr_str = f"ORI   {rd}, {rs1}, {imm}"
            case "111": instr_str = f"ANDI  {rd}, {rs1}, {imm}"

    elif op == "0000011":  # Loads
        match funct3:
            case "000": instr_str = f"LB   {rd}, {imm}({rs1})"
            case "001": instr_str = f"LH   {rd}, {imm}({rs1})"
            case "010": instr_str = f"LW   {rd}, {imm}({rs1})"
            case "100": instr_str = f"LBU  {rd}, {imm}({rs1})"
            case "101": instr_str = f"LHU  {rd}, {imm}({rs1})"

    elif op == "0100011":  # Stores
        match funct3:
            case "000": instr_str = f"SB   {rs2}, {imm}({rs1})"
            case "001": instr_str = f"SH   {rs2}, {imm}({rs1})"
            case "010": instr_str = f"SW   {rs2}, {imm}({rs1})"

    elif op == "1100011":  # Branches
        match funct3:
            case "000": instr_str = f"BEQ  {rs1}, {rs2}, offset {imm}"
            case "001": instr_str = f"BNE  {rs1}, {rs2}, offset {imm}"
            case "100": instr_str = f"BLT  {rs1}, {rs2}, offset {imm}"
            case "101": instr_str = f"BGE  {rs1}, {rs2}, offset {imm}"
            case "110": instr_str = f"BLTU {rs1}, {rs2}, offset {imm}"
            case "111": instr_str = f"BGEU {rs1}, {rs2}, offset {imm}"

    elif op == "0110111":  # LUI
        instr_str = f"LUI  {rd}, {imm}"

    elif op == "0010111":  # AUIPC
        instr_str = f"AUIPC  {rd}, {imm}"

    elif op == "1101111":  # JAL
        instr_str = f"JAL  {rd}, offset {imm}"

    elif op == "1100111":  # JALR
        instr_str = f"JALR {rd}, {imm}({rs1})"

    print(f"--> Decoded Instruction: {instr_str}")


#Populate the below functions as in the example lines of code to print your values for debugging
def Log_Datapath(dut,logger):
    #Log whatever signal you want from the datapath, called before positive clock edge
    logger.debug("************ DUT DATAPATH Signals ***************")
    dut._log.info("RegWrite:%s", ToHex(dut.dp.RegWrite.value))
    dut._log.info("Result:%s", ToHex(dut.dp.Result.value))


def Log_Controller(dut,logger):
    #Log whatever signal you want from the controller, called before positive clock edge
    logger.debug("************ DUT Controller Signals ***************")
    #dut._log.info("Op:%s", ToHex(dut.my_controller.Op.value))
    #dut._log.info("Funct:%s", ToHex(dut.my_controller.Funct.value))
    #dut._log.info("Rd:%s", ToHex(dut.my_controller.Rd.value))
    #dut._log.info("Src2:%s", ToHex(dut.my_controller.Src2.value))
    #dut._log.info("PCSrc:%s", ToHex(dut.my_controller.PCSrc.value))
    #dut._log.info("RegWrite:%s", ToHex(dut.my_controller.RegWrite.value))
    #dut._log.info("MemWrite:%s", ToHex(dut.my_controller.MemWrite.value))
    #dut._log.info("nPCSrc:%s", ToHex(dut.my_controller.nPCSrc.value))
    #dut._log.info("nRegWrite:%s", ToHex(dut.my_controller.nRegWrite.value))
    #dut._log.info("nMemWrite:%s", ToHex(dut.my_controller.nMemWrite.value))
    #dut._log.info("ALUSrc:%s", ToHex(dut.my_controller.ALUSrc.value))
    #dut._log.info("MemtoReg:%s", ToHex(dut.my_controller.MemtoReg.value))
    #dut._log.info("ALUControl:%s", ToHex(dut.my_controller.ALUControl.value))
    #dut._log.info("FlagWrite:%s", ToHex(dut.my_controller.FlagWrite.value))
    #dut._log.info("ImmSrc:%s", ToHex(dut.my_controller.ImmSrc.value))
    #dut._log.info("RegSrc:%s", ToHex(dut.my_controller.RegSrc.value))
    #dut._log.info("ALUFlags:%s", ToHex(dut.my_controller.ALUFlags.value))
    #dut._log.info("ShiftControl:%s", ToHex(dut.my_controller.ShiftControl.value))
    #dut._log.info("shamt:%s", ToHex(dut.my_controller.shamt.value))
    #dut._log.info("CondEx:%s", ToHex(dut.my_controller.CondEx.value))