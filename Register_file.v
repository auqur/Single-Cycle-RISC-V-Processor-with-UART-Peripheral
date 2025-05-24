module Register_file #(parameter WIDTH = 32)(
    input clk,
    input write_enable,
    input reset,
    input [4:0] Source_select_0,
    input [4:0] Source_select_1,
    input [4:0] Debug_Source_select,
    input [4:0] Destination_select,
    input [WIDTH-1:0] DATA,
    output [WIDTH-1:0] out_0,
    output [WIDTH-1:0] out_1,
    output [WIDTH-1:0] Debug_out
);

wire [WIDTH-1:0] Reg_Out [31:0];
wire [31:0] Reg_enable;

Register_rsten #(WIDTH) Reg0 (.clk(clk), .reset(reset), .we(1'b0), .DATA(DATA), .OUT(Reg_Out[0]));

genvar i;
generate
    for (i = 1 ; i < 31 ; i = i + 1) begin : registers
        Register_rsten #(WIDTH) Reg (.clk(clk), .reset(reset), .we(Reg_enable[i] & write_enable), .DATA(DATA), .OUT(Reg_Out[i]));
    end
endgenerate

assign out_0       = Reg_Out[Source_select_0];
assign out_1       = Reg_Out[Source_select_1];
assign Debug_out   = Reg_Out[Debug_Source_select];

endmodule
