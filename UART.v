module uart_peripheral (
    input         clk,
    input         reset,
    input         rx,              // Serial input line from external device
    input         tx_start,
    input  [7:0]  tx_data,
    input         read_rx,         // Reading request from PC
    input  [15:0] clk_per_bit,     // Clock cycles per bit
    output [31:0]  output_data,
    output        tx,              // Serial output line to external device
    output        tx_busy
);


    wire        lowword;
    wire [7:0]  fifo_read_data;

    wire rx_ready;
    wire [7:0] rx_byte;

    // UART RX instance
    uart_rx rx_inst (
        .clk(clk),
        .reset(reset),
        .rx(rx),
        .clk_per_bit(clk_per_bit),
        .rx_ready(rx_ready),
        .rx_data(rx_byte)
    );

    // FIFO buffer for RX
    fifo_buffer_16 rx_fifo (
        .clk(clk),
        .reset(reset),
        .write_req(rx_ready),
        .write_data(rx_byte),
        .read_req(read_rx),
        .read_data(fifo_read_data),
        .lowword(lowword)
    );

    assign output_data = (lowword) ? 32'hFFFFFFFF : {24'b0, fifo_read_data};

    // UART TX instance
    uart_tx tx_inst (
        .clk(clk),
        .reset(reset),
        .tx_start(tx_start),
        .tx_data(tx_data),
        .clk_per_bit(clk_per_bit),
        .tx(tx),
        .tx_busy(tx_busy)
    );

endmodule
