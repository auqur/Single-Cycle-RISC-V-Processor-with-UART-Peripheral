module Decoder_5to32 (
    input [4:0] IN,
    
    output reg [31:0] OUT
);

always @(*) begin
    OUT = 32'b1 << IN;
end

endmodule
