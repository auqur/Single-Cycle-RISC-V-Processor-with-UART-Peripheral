module UART_RX (
    input        UART_CLK,         
    input        reset,      
    input        rx,          
    output reg   rx_ready,    // High for one UART_CLK cycle when data is ready
    output reg [7:0] rx_data  // Received byte
);

    localparam [13:0] clock_baudrate_fix = 14'd10416;

    reg [3:0]  bit_index = 0;
    reg [15:0] clk_count = 0;
    reg [7:0]  rx_shift_reg = 0;
    reg        receiving = 0;
    reg        rx_sync = 1;

    // Double-sample input for metastability
    always @(posedge UART_CLK) begin
        rx_sync <= rx;
    end

    always @(posedge UART_CLK or posedge reset) begin
        if (reset) begin
            receiving <= 0;
            clk_count <= 0;
            bit_index <= 0;
            rx_shift_reg <= 0;
            rx_ready <= 0;
        end else begin
            rx_ready <= 0;

            if (!receiving) begin
                // Detect start bit (falling edge)
                if (rx_sync == 0) begin
                    receiving <= 1;
                    clk_count <= clock_baudrate_fix >> 1;  // Middle of start bit
                    bit_index <= 0;
                end
            end
            else begin
                if (clk_count == 0) begin
                    clk_count <= clock_baudrate_fix - 1;

                    if (bit_index < 8) begin
                        rx_shift_reg[bit_index] <= rx_sync;
                        bit_index <= bit_index + 1;
                    end 
                    else if (bit_index == 8) begin
                        // Stop bit, no need to store
                        bit_index <= bit_index + 1;
                    end 
                    else begin
                        // Done
                        receiving <= 0;
                        rx_data <= rx_shift_reg;
                        rx_ready <= 1;
                    end
                end 
                else begin
                    clk_count <= clk_count - 1;
                end
            end
        end
    end
endmodule
