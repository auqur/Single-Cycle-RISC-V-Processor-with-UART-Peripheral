module UART_RX (
    input UART_CLK,
    input reset,
    input rx,
    output reg [7:0] rx_data,
    output reg rx_ready
);
    reg [1:0] fsm;
    reg [3:0] bit_index;
    reg [7:0] shift_reg;
    reg [13:0] clk_count;

    initial begin
        fsm = 2'b00;
        bit_index = 4'b0000;
        shift_reg = 8'b00000000;
        clk_count = 14'b00000000000000;
    end

    localparam clk_by_baudrate = 10416;

    always @(posedge UART_CLK or posedge reset) begin
        if (reset) begin
            clk_count <= 0;
            fsm <= 2'b00;
            shift_reg <= 0;
            bit_index <= 0;
            rx_ready <= 0;
            rx_data <= 0;
        end else begin
            rx_ready <= 0;

            case(fsm)
                2'b00: begin    // Idle state, waiting for start bit
                    if (rx == 0) begin 
                        fsm <= 2'b01;
                        clk_count <= clk_by_baudrate / 2; // Start counting for the middle of the start bit
                    end
                end

                2'b01: begin    // Start bit state. Waiting for the start bit to stabilize
                    if (clk_count == 0) begin
                        if (rx == 0) begin 
                            fsm <= 2'b10;
                            clk_count <= clk_by_baudrate - 1;
                            bit_index <= 0;
                        end 
                        else begin
                            fsm <= 2'b00; // If the line is not low, go back to idle
                        end
                    end 
                    else begin
                        clk_count <= clk_count - 1;
                    end
                end

                2'b10: begin    // Data bit state. Collecting data bits
                    if (clk_count == 0) begin
                        shift_reg[bit_index] <= rx;
                        clk_count <= clk_by_baudrate - 1;
                        bit_index <= bit_index + 1;

                        if (bit_index == 7) begin
                            fsm <= 2'b11;
                        end
                    end 
                    else begin
                        clk_count <= clk_count - 1;
                    end
                end

                2'b11: begin    // Stop bit state. Waiting for the stop bit
                    if (clk_count == 0) begin
                        if (rx == 1) begin 
                            rx_data <= shift_reg;
                            rx_ready <= 1;
                        end
                        fsm <= 2'b00;
                    end 
                    else begin
                        clk_count <= clk_count - 1;
                    end
                end

            endcase
        end
    end
endmodule

