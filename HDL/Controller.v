module Controller
(
    input  clk, reset,
    input  Zero,
    input  [31:0] Instr, RF_OUT1, RF_OUT2,

    output  PCSrc, RegWrite, ResultSrc, RF_WD_SRC,
    output  [1:0] MemWrite, ALUSrc,
    output  [2:0] ImmSrc, READMODE,
    output  [3:0] ALUControl
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


//Comparator
wire EQ, NE, LT, GE, LTU, GEU;
assign EQ = (RF_OUT1 == RF_OUT2);
assign NE = (RF_OUT1 != RF_OUT2);
assign LT = ($signed(RF_OUT1) < $signed(RF_OUT2));
assign GE = ($signed(RF_OUT1) >= $signed(RF_OUT2));
assign LTU = (RF_OUT1 < RF_OUT2);
assign GEU = (RF_OUT1 >= RF_OUT2);

//PCSrc
assign PCSrc = (op == JAL_INSTR | op == JALR_INSTR) ? 1'b1 :
               (op == BRANCH_INSTR) ? ((funct3 == BEQ) ? EQ :
                                      (funct3 == BNE) ? NE :
                                      (funct3 == BLT) ? LT :
                                      (funct3 == BGE) ? GE :
                                      (funct3 == BLTU) ? LTU :
                                      (funct3 == BGEU) ? GEU : 1'b0) :
                1'b0;

//RegWrite
assign RegWrite = (op == REG_REG_INSTR | op == REG_IMM_INSTR | op == MEM_LOAD_INSTR | op == LUI_INSTR | op == AUIPC_INSTR | op == JAL_INSTR | op == JALR_INSTR);

//ResultSrc
assign ResultSrc = (op == MEM_LOAD_INSTR);
 
//RF_WD_SRC
assign RF_WD_SRC = (op == JAL_INSTR | op == JALR_INSTR);

//MemWrite
assign MemWrite = (op == MEM_STORE_INSTR) ? 
                  ((funct3 == SB) ? 2'b11 : 
                   (funct3 == SH) ? 2'b10 : 
                   (funct3 == SW) ? 2'b01 : 2'b00) : 
                  2'b00;

//ImmSrc
assign ImmSrc = (op == REG_IMM_INSTR & funct3 == SLTIU) ? 3'b001 :  //UEX12
                (op == BRANCH_INSTR ) ? 3'b010 :    //B_IMM
                (op == JAL_INSTR) ? 3'b011 : //JALEX
                (op == LUI_INSTR | op == AUIPC_INSTR) ? 3'b100 : //U_IMM
                (op == MEM_STORE_INSTR) ? 3'b101 : // S_IMM
                3'b000; //default is SEX12

//READMODE
assign READMODE = (op == MEM_LOAD_INSTR) ? 
                  ((funct3 == LB) ? 3'b110 : 
                   (funct3 == LH) ? 3'b011 : 
                   (funct3 == LW) ? 3'b000 : 
                   (funct3 == LBU) ? 3'b010 : 
                   (funct3 == LHU) ? 3'b001 : 3'b000) : 
                  3'b000; //default is WORD

//ALUSrc
assign ALUSrc[0] = ((op == BRANCH_INSTR) | (op == AUIPC_INSTR) | (op == JAL_INSTR));
assign ALUSrc[1] = (op == REG_IMM_INSTR | op == MEM_LOAD_INSTR | op == MEM_STORE_INSTR | op == JALR_INSTR | op == BRANCH_INSTR | op == LUI_INSTR | op == AUIPC_INSTR | op == JAL_INSTR);

//ALUControl
assign ALUControl[3:1] = (op == REG_REG_INSTR | op == REG_IMM_INSTR ) ? funct3 : 3'b0;
assign ALUControl[0] = (op == REG_REG_INSTR | op == REG_IMM_INSTR ) ? (funct7 == 7'b0100000) : 1'b0;

endmodule
//iverilog -o Controller.out Controller.v