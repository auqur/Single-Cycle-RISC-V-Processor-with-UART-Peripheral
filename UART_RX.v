module UART_RX (
    input        clk,         // System clock
    input        reset,       // Asynchronous reset
    input        rx,          // Serial input line
    input [15:0] clk_per_bit, // Clock cycles per bit (baud rate)
    output reg   rx_ready,    // High for one clk cycle when data is ready
    output reg [7:0] rx_data  // Received byte
);

    reg [3:0]  bit_index = 0;
    reg [15:0] clk_count = 0;
    reg [7:0]  rx_shift = 0;
    reg        receiving = 0;
    reg        rx_sync = 1;

    // Double-sample input for metastability
    always @(posedge clk) begin
        rx_sync <= rx;
    end

    always @(posedge clk or posedge reset) begin
        if (reset) begin
            receiving <= 0;
            clk_count <= 0;
            bit_index <= 0;
            rx_shift <= 0;
            rx_ready <= 0;
        end else begin
            rx_ready <= 0;

            if (!receiving) begin
                // Detect start bit (falling edge)
                if (rx_sync == 0) begin
                    receiving <= 1;
                    clk_count <= clk_per_bit >> 1;  // Middle of start bit
                    bit_index <= 0;
                end
            end else begin
                if (clk_count == 0) begin
                    clk_count <= clk_per_bit - 1;

                    if (bit_index < 8) begin
                        rx_shift[bit_index] <= rx_sync;
                        bit_index <= bit_index + 1;
                    end else if (bit_index == 8) begin
                        // Stop bit, no need to store
                        bit_index <= bit_index + 1;
                    end else begin
                        // Done
                        receiving <= 0;
                        rx_data <= rx_shift;
                        rx_ready <= 1;
                    end
                end else begin
                    clk_count <= clk_count - 1;
                end
            end
        end
    end
endmodule
