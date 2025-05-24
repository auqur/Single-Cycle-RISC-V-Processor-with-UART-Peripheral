module ALU #(parameter WIDTH = 32)(
    input [3:0] control,
    input [WIDTH-1:0] DATA_A,
    input [WIDTH-1:0] DATA_B,
    output reg [WIDTH-1:0] OUT,
    output reg Zero
);

localparam  ADD  = 4'b0000,
            SUB  = 4'b0001,
            AND_ = 4'b1110,
            OR_  = 4'b1100,
            XOR_ = 4'b1000,
            SLL  = 4'b0010,
            SRL  = 4'b1010,
            SRA  = 4'b1011,
            SLT  = 4'b0100,
            SLTU = 4'b0110;

always @(*) begin
    case (control)
        ADD:   OUT = DATA_A + DATA_B;
        SUB:   OUT = DATA_A - DATA_B;
        SLL:   OUT = DATA_A << DATA_B[4:0];
        SLT:   OUT = ($signed(DATA_A) < $signed(DATA_B)) ? {{(WIDTH-1){1'b0}},1'b1} : {WIDTH{1'b0}};
        SLTU:  OUT = (DATA_A < DATA_B) ? {{(WIDTH-1){1'b0}},1'b1} : {WIDTH{1'b0}};
        XOR_:  OUT = DATA_A ^ DATA_B;
        SRL:   OUT = DATA_A >> DATA_B[4:0];
        SRA:   OUT = $signed(DATA_A) >>> DATA_B[4:0];
        OR_:   OUT = DATA_A | DATA_B;
        AND_:  OUT = DATA_A & DATA_B;
        default: OUT = {WIDTH{1'b0}};
    endcase

    Zero = (OUT == {WIDTH{1'b0}}) ? 1'b1 : 1'b0;
end

endmodule

//iverilog -o ALU.out ALU.v
