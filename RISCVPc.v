module RISCVPc
(
    input wire clk, reset,
    input wire [4:0] Debug_Source_select,
    input wire [31:0] Debug_out,
    output wire [31:0] PC
);

wire PCSrc, RegWrite, ResultSrc, RF_WD_SRC, Zero;
wire [1:0] MemWrite, ALUSrc;
wire [2:0] ImmSrc, READMODE;
wire [3:0] ALUControl;
wire [31:0] Instr, RF_OUT1, RF_OUT2;
Datapath dp
(   clk, reset, PCSrc, RegWrite, ResultSrc, RF_WD_SRC,
    MemWrite, ALUSrc,
    ImmSrc, READMODE,
    ALUControl,
    Debug_Source_select,

    Zero,
    PC, Instr,
    Debug_out,  RF_OUT1, RF_OUT2
);

Controller ctrl
(   clk, reset,
    Zero,
    Instr, RF_OUT1, RF_OUT2,

    PCSrc, RegWrite, ResultSrc, RF_WD_SRC,
    MemWrite, ALUSrc,
    ImmSrc, READMODE,
    ALUControl
);
endmodule

//iverilog -o RISCVPc.out RISCVPc.v Controller.v Datapath.v Mux_2to1.v Register_file.v Register_reset.v Register_rsten.v Adder.v Extender.v ALU.v Memory.v Instruction_memory.v