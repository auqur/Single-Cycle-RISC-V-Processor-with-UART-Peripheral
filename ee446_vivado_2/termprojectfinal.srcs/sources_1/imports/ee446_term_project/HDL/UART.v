module UART (
    input         UART_CLK,
    input         BUTTON_CLK,
    input         reset,
    input         rx,              // Serial input line from external device
    input         tx_start,
    input  [7:0]  tx_data,
    input         read_rx,         // Reading request from PC
    output [31:0]  output_data,
    output        tx           // Serial output line to external device
);
    wire        lowword;
    wire [7:0]  fifo_read_data;

    wire rx_ready;
    wire [7:0] rx_byte;

    reg tx_start_prev;
    wire tx_start_rising;
    
    //For transmitting one data per instruction
    always @(posedge UART_CLK or posedge reset) begin
        if (reset) begin
            tx_start_prev <= 0;
        end else begin
            tx_start_prev <= tx_start;
        end
    end

    assign tx_start_rising = tx_start & ~tx_start_prev;

    // UART RX instance
    UART_RX rx_inst (
        .UART_CLK(UART_CLK),
        .reset(reset),
        .rx(rx),
        .rx_ready(rx_ready),
        .rx_data(rx_byte)
    );

    // FIFO buffer for RX
    UART_FIFO_BUFFER rx_fifo (
        .UART_CLK(UART_CLK),
        .BUTTON_CLK(BUTTON_CLK),
        .reset(reset),
        .write_req(rx_ready),
        .write_data(rx_byte),
        .read_req(read_rx),
        .read_data(fifo_read_data),
        .lowword(lowword)
    );

    assign output_data = (lowword) ? 32'hFFFFFFFF : {24'b0, fifo_read_data};

    // UART TX instance
    UART_TX tx_inst (
        .UART_CLK(UART_CLK),
        .reset(reset),
        .tx_start(tx_start_rising),
        .tx_data(tx_data),
        .tx(tx)
    );

endmodule