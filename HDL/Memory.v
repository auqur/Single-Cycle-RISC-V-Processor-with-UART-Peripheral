module Memory#(parameter BYTE_SIZE=4, parameter ADDR_WIDTH=32)
(
    input clk,
    input [1:0] WE,
    input [2:0] READMODE,
    input [ADDR_WIDTH-1:0] ADDR,
    input [(BYTE_SIZE*8)-1:0] WD,

    output reg [(BYTE_SIZE*8)-1:0] RD
);

reg [7:0] mem [255:0];
integer i, k;

initial begin
    for (i = 0; i < 256; i = i + 1) begin
        mem[i] = 8'b0;
    end
end

always @(*) begin
    case(READMODE)
        3'b000: begin // Word read
            for (i = 0; i < BYTE_SIZE; i = i + 1)
                RD[8*i+:8] = mem[ADDR+i];
        end
        3'b001: begin // Half-word Unsigned read
            for (i = 0; i < BYTE_SIZE / 2; i = i + 1)
                RD[8*i+:8] = mem[ADDR+i];
            RD[31:16] = 16'b0;
        end
        3'b011: begin // Half-word Signed read
            for (i = 0; i < BYTE_SIZE / 2; i = i + 1)
                RD[8*i+:8] = mem[ADDR+i];
            RD[31:16] = {16{RD[15]}};
        end
        3'b010: begin // Byte Unsigned read
            for (i = 0; i < BYTE_SIZE / 4; i = i + 1)
                RD[8*i+:8] = mem[ADDR+i];
            RD[31:8] = 24'b0;
        end
        3'b110: begin // Byte Signed read
                for (i = 0; i < BYTE_SIZE / 4; i = i + 1)
                RD[8*i+:8] = mem[ADDR+i];
            RD[31:8] = {24{RD[7]}};
        end
        default: RD = {(BYTE_SIZE*8){1'b0}};
    endcase
end

always @(posedge clk) begin
    if (WE == 2'b01) begin // Word write
        for (k = 0; k < BYTE_SIZE; k = k + 1)
            mem[ADDR+k] <= WD[8*k+:8];
    end
    else if (WE == 2'b10) begin // Half-word write
        for (k = 0; k < BYTE_SIZE / 2; k = k + 1)
            mem[ADDR+k] <= WD[8*k+:8];
    end
    else if (WE == 2'b11) begin // Byte write
        mem[ADDR] <= WD[7:0];
    end
end

endmodule
