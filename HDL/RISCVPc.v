module RISCVPc (
    input  clk, reset,
    input  [4:0] Debug_Source_select,
    input  [31:0] Debug_out,
    output [31:0] Debug_PC
);

wire PCSrc, RegWrite, ResultSrc, RF_WD_SRC, Zero;
wire [1:0] MemWrite, ALUSrc;
wire [2:0] ImmSrc, READMODE;
wire [3:0] ALUControl;
wire [31:0] Instr, RF_OUT1, RF_OUT2, PC;

assign Debug_PC = PC;

Datapath dp (
    .clk(clk),
    .reset(reset),
    .PCSrc(PCSrc),
    .RegWrite(RegWrite),
    .ResultSrc(ResultSrc),
    .RF_WD_SRC(RF_WD_SRC),
    .MemWrite(MemWrite),
    .ALUSrc(ALUSrc),
    .ImmSrc(ImmSrc),
    .READMODE(READMODE),
    .ALUControl(ALUControl),
    .Debug_Source_select(Debug_Source_select),
    .Zero(Zero),
    .PC(PC),
    .Instr(Instr),
    .Debug_out(Debug_out),
    .RF_OUT1(RF_OUT1),
    .RF_OUT2(RF_OUT2)
);

Controller ctrl (
    .clk(clk),
    .reset(reset),
    .Zero(Zero),
    .Instr(Instr),
    .RF_OUT1(RF_OUT1),
    .RF_OUT2(RF_OUT2),
    .PCSrc(PCSrc),
    .RegWrite(RegWrite),
    .ResultSrc(ResultSrc),
    .RF_WD_SRC(RF_WD_SRC),
    .MemWrite(MemWrite),
    .ALUSrc(ALUSrc),
    .ImmSrc(ImmSrc),
    .READMODE(READMODE),
    .ALUControl(ALUControl)
);

endmodule
