module UART_TX (
    input        UART_CLK,         
    input        reset,       
    input        tx_start,    
    input  [7:0] tx_data,     
    output reg   tx            
);
    localparam [13:0] clock_baudrate_fix = 14'd10416;

    reg tx_busy;
    reg [3:0] bit_index;     
    reg [15:0] clk_count;     
    reg [9:0] shift_reg;      

    always @(posedge UART_CLK) begin
        if (reset) begin
            tx <= 1'b1;        // Idle state is HIGH
            tx_busy <= 0;
            clk_count <= 0;
            bit_index <= 0;
            shift_reg <= 10'b1111111111;
        end 
        else begin
            if (tx_start && !tx_busy) begin
                // Load transmit frame: start bit (0), 8 data bits, stop bit (1)
                shift_reg <= {1'b1, tx_data, 1'b0};
                tx_busy <= 1;
                bit_index <= 0;
                clk_count <= 0;
            end 
            else if (tx_busy) begin
                if (clk_count < clock_baudrate_fix - 1) begin
                    clk_count <= clk_count + 1;
                end 
                else begin
                    clk_count <= 0;
                    tx <= shift_reg[bit_index];
                    bit_index <= bit_index + 1;

                    if (bit_index == 9) begin
                        tx_busy <= 0;
                        tx <= 1'b1; // Return to idle
                    end
                end
            end
        end
    end

endmodule
