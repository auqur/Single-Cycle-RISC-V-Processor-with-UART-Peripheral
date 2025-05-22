module Controller
(
    input clk, reset,
    input Zero,
    input [31:0] Instr,


    output reg PCSrc, RegWrite, ALUSrc, ResultSrc,
    output reg [1:0] MemWrite,
    output reg [2:0] ImmSrc,
    output reg [3:0] ALUControl
);


//opcode
localparam  LUI_INSTR       = 7'b0110111,
            AUIPC_INSTR     = 7'b0010111,
            JAL_INSTR       = 7'b1101111,
            BRANCH_INSTR    = 7'b1100011,
            JALR_INSTR      = 7'b1100111,
            MEM_LOAD_INSTR  = 7'b0000011,
            REG_IMM_INSTR   = 7'b0010011,
            MEM_STORE_INSTR = 7'b0100011,
            CNST_SHFT_INSTR = 7'b0010011,
            REG_REG_INSTR   = 7'b0110011;

//f3
localparam  BEQ  = 3'b000,
            BNE  = 3'b001,
            BLT  = 3'b100,
            BGE  = 3'b101,
            BLTU = 3'b110,
            BGEU = 3'b111;
//f3
localparam  LB  = 3'b000,
            LH  = 3'b001,
            LW  = 3'b010,
            LBU = 3'b100,
            LHU = 3'b101;
//f3
localparam  ADDI  = 3'b000,
            SLTI  = 3'b010,
            SLTIU = 3'b011,
            XORI  = 3'b100,
            ORI   = 3'b110,
            ANDI  = 3'b111;
//f3
localparam  SB = 3'b000,
            SH = 3'b001,
            SW = 3'b010;
//{f7,f3}
localparam  SLLI = {7'b0000000, 3'b001},
            SRLI = {7'b0000000, 3'b101},
            SRAI = {7'b0100000, 3'b101};
//{f7,f3}
localparam  ADD  = {7'b0000000, 3'b000},
            SUB  = {7'b0100000, 3'b000},
            SLL  = {7'b0000000, 3'b001},
            SLT  = {7'b0000000, 3'b010},
            SLTU = {7'b0000000, 3'b011},
            XOR_ = {7'b0000000, 3'b100},
            SRL  = {7'b0000000, 3'b101},
            SRA  = {7'b0100000, 3'b101},
            OR_  = {7'b0000000, 3'b110},
            AND_ = {7'b0000000, 3'b111};

wire [6:0] op;
wire [4:0] rd, rs1, rs2;
wire [2:0] funct3;
wire [6:0] funct7;

assign op = Instr[6:0];
assign rd = Instr[11:7];
assign rs1 = Instr[19:15];
assign rs2 = Instr[24:20];
assign funct3 = Instr[14:12];
assign funct7 = Instr[31:25];

initial begin
    PCSrc = 1'b0;
    RegWrite = 1'b0;
    ALUSrc = 1'b0;
    ResultSrc = 1'b0;
    MemWrite = 2'b00;
    ImmSrc = 3'b000;
    ALUControl = 4'b0000;
end

//ALUControl
assign ALUContro[3:1] = (op == REG_REG_INST | op == REG_IMM_INSTR | op == CNST_SHFT_INSTR ) ? funct3 :
                        3'b0;
assign ALUControl[0] = (op == REG_REG_INST | op == REG_IMM_INSTR | op == CNST_SHFT_INSTR ) ? (funct7 == 7'b0100000) :
                        1'b0;



endmodule