module Extender (
    input [31:0]DATA,
    input [2:0]select,

    output reg [31:0]Extended_data
);

localparam 	SEX12 = 3'b000,
            UEX12 = 3'b001,
            B_IMM = 3'b010,
            JALEX = 3'b011,
            U_IMM = 3'b100,
            S_IMM = 3'b101;

always @(*) begin
    case (select)

        SEX12: Extended_data = {{21{DATA[31]}}, DATA[30:20]};

        UEX12: Extended_data = {20'b0, DATA[31:20]};

        B_IMM: Extended_data = {{20{DATA[31]}}, DATA[7], DATA[30:25], DATA[11:8], 1'b0};

        JALEX: Extended_data = {{12{DATA[31]}}, DATA[19:12], DATA[20], DATA[30:21], 1'b0};

        U_IMM: Extended_data = {DATA[31:12], 12'b0};

        S_IMM: Extended_data = {{21{DATA[31]}}, DATA[30:25], DATA[11:7]};
        
        default: Extended_data = 32'd0;
    endcase
end
    
endmodule