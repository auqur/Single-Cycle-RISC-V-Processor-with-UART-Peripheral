module Datapath
(
    input clk, reset,
    input PCSrc, RegWrite, ResultSrc, RF_WD_SRC,
    input [1:0] MemWrite, shctrl, ALUSrc,
    input [2:0] ImmSrc, READMODE,
    input [3:0] ALUControl,
    input [4:0] Debug_Source_select,

    output Zero,
    output [31:0] PC, Instr,
    output [31:0] Debug_out,  RF_OUT1, RF_OUT2, ImmExt
);

wire [31:0] PCNext, PCPlus4, PCTarget, RF_WD;
wire [31:0] SrcA, SrcB,;
wire [31:0] ReadData;
wire [31:0] Result;
wire [31:0] ALUResult;

Register_reset #(32) PC_Register
(
    .clk(clk),
    .reset(reset),
    .DATA(PCNext),
    .OUT(PC)
);

Adder #(32) PCAdder
(
    .DATA_A(PC),
    .DATA_B(32'd4),
    .OUT(PCPlus4)
);

Mux_2to1 #(32) PCSrcMux
(
    .select(PCSrc),
    .input_0(PCPlus4),
    .input_1(Result),
    .output_value(PCNext)
);

Inst_Memory #(4,32) Instruction_Memory
(
    .ADDR(PC),
    .RD(Instr)
);

Mux_2to1 #(32) RF_DATA_MUX
(
    .select(RF_WD_SRC),
    .input_0(Result),
    .input_1(PCPlus4),
    .output_value(RF_WD)
);

Register_file #(32) Register_File
(
    .clk(clk),
    .write_enable(RegWrite),
    .reset(reset),
    .Source_select_0(Instr[19:15]), //rs1
    .Source_select_1(Instr[24:20]), //rs2
    .Debug_Source_select(Debug_Source_select),
    .Destination_select(Instr[11:7]), //rd
    .DATA(RF_WD),
    .out_0(RF_OUT1),
    .out_1(RF_OUT2),
    .Debug_out(Debug_out)
);

Extender extender
(
    .DATA(Instr[31:0]),
    .select(ImmSrc),
    .Extended_data(ImmExt)
);

Mux_2to1 #(32) SrcAMux
(
    .select(ALUSrc[0]),
    .input_0(RF_OUT1),
    .input_1(PC),
    .output_value(SrcA)
);

Mux_2to1 #(32) SrcB_Mux
(
    .select(ALUSrc[1]),
    .input_0(RF_OUT2),
    .input_1(ImmExt),
    .output_value(SrcB)
);

ALU #(32) ALU_Unit
(
    .control(ALUControl),
    .DATA_A(SrcA),
    .DATA_B(SrcB),
    .OUT(ALUResult),
    .Zero(Zero)
);

Memory #(4, 32) Data_Memory
(
    .clk(clk),
    .WE(MemWrite),
    .READMODE(READMODE),
    .ADDR(ALUResult),
    .WD(WriteData),
    .RD(ReadData)
);

Mux_2to1 #(32) WriteData_Mux
(
    .select(ResultSrc),
    .input_0(ALUResult),
    .input_1(ReadData),
    .output_value(Result)
);

endmodule