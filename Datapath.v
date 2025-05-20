module Datapath
(
    input clk, reset,
    inout PCSrc, RegWrite, ALUSrc, ResultSrc,
    input [1:0] MemWrite,
    input [2:0] ImmSrc,
    input [3:0] ALUControl,
    input [4:0] Debug_Source_select,

    output Zero,
    output [31:0] PC, Instr,
    output [31:0] Debug_out
);

wire [31:0] PCNext, PCPlus4, PCTarget;
wire [31:0] SrcA, SrcB;
wire [31:0] WriteData, ReadData;
wire [31:0] Result;
wire [31:0] ImmExt;
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
    .input_1(PCTarget),
    .output_value(PCNext)
);

Inst_Memory #(4,32) Instruction_Memory
(
    .ADDR(PC),
    .RD(Instr)
);

Register_file #(32) Register_File
(
    .clk(clk),
    .write_enable(RegWrite),
    .reset(reset),
    .Source_select_0(Instr[19:15]),
    .Source_select_1(Instr[24:20]),
    .Debug_Source_select(Debug_Source_select),
    .Destination_select(Instr[11:7]),
    .DATA(Result),
    .out_0(SrcA),
    .out_1(WriteData),
    .Debug_out(Debug_out)
);

Extender extender
(
    .DATA(Instr[31:0]),
    .select(ImmSrc),
    .Extended_data(ImmExt)
);

Mux_2to1 #(32) SrcB_Mux
(
    .select(ALUSrc),
    .input_0(WriteData),
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