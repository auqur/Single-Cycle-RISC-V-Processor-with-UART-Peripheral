module RISCVPc
(
    input wire clk, reset,
    input wire [31:0] Instr,
    output reg [31:0] PC
);

