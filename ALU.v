module ALU #(parameter WIDTH=8)
(
	input [3:0] control,
	input [4:0] shamt,
	input [WIDTH-1:0] DATA_A,
	input [WIDTH-1:0] DATA_B,
	output reg [WIDTH-1:0] OUT,
);
localparam 	ADD = 4'b0000,
			SUB = 4'b0001,
			SLL = 4'b0010,
			SLT = 4'b0011,
			SLTU = 4'b0100,
			XOR = 4'b0101,
			SRL = 4'b0110,
			SRA = 4'b0111,
			OR = 4'b1000,
			AND = 4'b1001

always@(*) begin
	case(control)
		ADD: OUT = DATA_A + DATA_B;
		SUB: OUT = DATA_A - DATA_B;
		SLL: OUT = DATA_A << shamt;
		SLT: OUT = (DATA_A < DATA_B) ? 32'd1 : 32'd0;
		SLTU: OUT = (DATA_A < DATA_B) ? 32'd1 : 32'd0;
		XOR: OUT = DATA_A ^ DATA_B;
		SRL: OUT = DATA_A >> shamt;
		SRA: OUT = $signed(DATA_A) >>> shamt;
		OR:  OUT = DATA_A | DATA_B;
		AND: OUT = DATA_A & DATA_B;

	endcase
end

endmodule	 
