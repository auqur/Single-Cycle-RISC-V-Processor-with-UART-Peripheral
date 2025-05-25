

module Nexys_A7(
    //////////// GCLK //////////
    input wire                  CLK100MHZ,
	//////////// BTN //////////
	input wire		     		BTNU, 
	                      BTNL, BTNC, BTNR,
	                            BTND,
	//////////// SW //////////
	input wire	     [15:0]		SW,
	/////////// UART //////////
	input wire UART_TXD_IN,
	output wire UART_RXD_OUT,
	//////////// LED //////////
	output wire		 [15:0]		LED,
    //////////// 7 SEG //////////
    output wire [7:0] AN,
    output wire CA, CB, CC, CD, CE, CF, CG, DP
);

wire [31:0] reg_out, PC;
wire [4:0] buttons;

assign LED = SW;

MSSD mssd_0(
        .clk        (CLK100MHZ                      ),
        .value      ({PC[7:0], reg_out[23:0]}       ),
        .dpValue    (8'b01000000                    ),
        .display    ({CG, CF, CE, CD, CC, CB, CA}   ),
        .DP         (DP                             ),
        .AN         (AN                             )
    );

debouncer debouncer_0(
        .clk        (CLK100MHZ                      ),
        .buttons    ({BTNU, BTNL, BTNC, BTNR, BTND} ),
        .out        (buttons                        )
    );

RISCVPc  riscpcc(
    .clk(buttons[4]),
    .reset(buttons[0]),
    .UART_CLK(CLK100MHZ),
    .UART_RX(UART_TXD_IN), 
    .UART_TX(UART_RXD_OUT),
    .Debug_Source_select(SW[4:0]),
    .Debug_out(reg_out),
    .Debug_PC(PC)
);

endmodule
