module uart_peripheral (
    input         clk,
    input         reset,
    input         rx,
    input         tx_start,
    input  [7:0]  tx_data,
    input         read_rx,         // CPU reads received data
    input  [15:0] clk_per_bit,     // Clock cycles per bit
    output [7:0]  rx_data,
    output        rx_ready,        // Indicates valid data available
    output        tx,
    output        tx_busy
);

    wire        fifo_write_en;
    wire [7:0]  fifo_write_data;
    wire        fifo_empty;
    wire [7:0]  fifo_read_data;

    wire rx_ready_raw;
    wire [7:0] rx_byte;

    // UART RX instance
    uart_rx rx_inst (
        .clk(clk),
        .reset(reset),
        .rx(rx),
        .clk_per_bit(clk_per_bit),
        .rx_ready(rx_ready_raw),
        .rx_data(rx_byte)
    );

    // FIFO buffer for RX
    fifo_buffer_16 rx_fifo (
        .clk(clk),
        .reset(reset),
        .write_en(rx_ready_raw),
        .write_data(rx_byte),
        .read_en(read_rx),
        .read_data(fifo_read_data),
        .empty(fifo_empty),
        .full()
    );

    assign rx_data = fifo_read_data;
    assign rx_ready = ~fifo_empty;

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
